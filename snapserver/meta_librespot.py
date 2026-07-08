#!/usr/bin/env python3
"""Snapcast stream-plugin controlscript bridging librespot player events.

librespot runs standalone (see the librespot/ image) with --onevent, whose
hook serializes player events as JSON lines into a FIFO shared through the
compose 'shared_pipes' volume. This script tails that FIFO and forwards
playback state and track metadata to snapserver over the stream-plugin
JSON-RPC protocol on stdout/stdin.

librespot has no external control API, so every can* capability is reported
false and control requests are rejected; Snapweb shows metadata without
playback buttons.
"""

import argparse
import json
import sys
import threading
import time

DEFAULT_METADATA_PIPE = "/tmp/librespot-metadata"

state_lock = threading.Lock()
properties = {
    "playbackStatus": "stopped",
    "loopStatus": "none",
    "shuffle": False,
    "mute": False,
    "canControl": False,
    "canPlay": False,
    "canPause": False,
    "canSeek": False,
    "canGoNext": False,
    "canGoPrevious": False,
    "metadata": {},
}


def send(message):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def log(severity, message):
    send({
        "jsonrpc": "2.0",
        "method": "Plugin.Stream.Log",
        "params": {"severity": severity, "message": message},
    })


def notify_properties():
    with state_lock:
        params = dict(properties)
    send({
        "jsonrpc": "2.0",
        "method": "Plugin.Stream.Player.Properties",
        "params": params,
    })


def ms_to_seconds(value):
    try:
        return int(value) / 1000.0
    except (TypeError, ValueError):
        return None


def handle_event(event):
    kind = event.get("event")
    with state_lock:
        if kind == "track_changed":
            metadata = {}
            if event.get("name"):
                metadata["title"] = event["name"]
            if event.get("artists"):
                metadata["artist"] = event["artists"]
            if event.get("album"):
                metadata["album"] = event["album"]
            if event.get("covers"):
                metadata["artUrl"] = event["covers"][0]
            if event.get("track_id"):
                metadata["trackId"] = event["track_id"]
            duration = ms_to_seconds(event.get("duration_ms"))
            if duration is not None:
                metadata["duration"] = duration
            properties["metadata"] = metadata
        elif kind in ("playing", "paused", "stopped"):
            properties["playbackStatus"] = kind
            if kind == "stopped":
                properties["metadata"] = {}
        else:
            return
        position = ms_to_seconds(event.get("position_ms"))
        if position is not None:
            properties["position"] = position
        else:
            properties.pop("position", None)
    notify_properties()


def fifo_reader(path):
    while True:
        try:
            # Opening the FIFO blocks until a writer connects; each onevent
            # write closes the pipe again, so reopen on EOF forever.
            with open(path, "r", encoding="utf-8", errors="replace") as fifo:
                for line in fifo:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        handle_event(json.loads(line))
                    except (json.JSONDecodeError, TypeError) as exc:
                        log("Error", "bad metadata event: %s" % exc)
        except OSError as exc:
            log("Error", "metadata pipe %s unavailable (%s), retrying" % (path, exc))
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser()
    # Passed automatically by snapserver to every controlscript.
    parser.add_argument("--stream", default="")
    parser.add_argument("--snapcast-port", default="")
    parser.add_argument("--snapcast-host", default="")
    # Overridable via controlscriptparams in the stream URI.
    parser.add_argument("--metadata-pipe", default=DEFAULT_METADATA_PIPE)
    args, _ = parser.parse_known_args()

    threading.Thread(target=fifo_reader, args=(args.metadata_pipe,), daemon=True).start()

    send({"jsonrpc": "2.0", "method": "Plugin.Stream.Ready"})

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        request_id = request.get("id")
        method = request.get("method", "")
        if method == "Plugin.Stream.Player.GetProperties":
            with state_lock:
                result = dict(properties)
            send({"jsonrpc": "2.0", "id": request_id, "result": result})
        elif method in ("Plugin.Stream.Player.Control", "Plugin.Stream.Player.SetProperty"):
            send({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": "Stream cannot be controlled"},
            })
        elif request_id is not None:
            send({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": "Method not found"},
            })


if __name__ == "__main__":
    main()
