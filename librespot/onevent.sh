#!/bin/sh

# Called by librespot for every player event; forwards the ones relevant to
# metadata/playback state as a JSON line into the metadata FIFO, where the
# snapserver-side controlscript (meta_librespot.py) picks them up.
#
# librespot waits for this script to exit before dispatching the next event,
# so it must never block: the FIFO write is wrapped in a short timeout and
# the event is dropped when nobody is reading.

case "$PLAYER_EVENT" in
    track_changed|playing|paused|stopped) ;;
    *) exit 0 ;;
esac

# ARTISTS and COVERS arrive newline-separated; jq turns them into arrays and
# handles all JSON escaping of track names.
json=$(jq -cn \
    --arg event "$PLAYER_EVENT" \
    --arg name "${NAME:-}" \
    --arg artists "${ARTISTS:-}" \
    --arg album "${ALBUM:-}" \
    --arg covers "${COVERS:-}" \
    --arg duration_ms "${DURATION_MS:-}" \
    --arg track_id "${TRACK_ID:-}" \
    --arg position_ms "${POSITION_MS:-}" \
    '{
        event: $event,
        name: $name,
        artists: ($artists | split("\n") | map(select(. != ""))),
        album: $album,
        covers: ($covers | split("\n") | map(select(. != ""))),
        duration_ms: $duration_ms,
        track_id: $track_id,
        position_ms: $position_ms
    }')

printf '%s\n' "$json" | timeout 2 sh -c 'cat > "$METADATA_PIPE"' 2>/dev/null || true
