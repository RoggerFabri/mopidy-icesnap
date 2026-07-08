#!/usr/bin/dumb-init /bin/sh

env

set -x

# librespot's pipe backend opens its output with create=true: if the FIFO is
# missing it silently writes a growing regular file instead, so both pipes
# must exist as FIFOs before playback starts.
for p in "$PIPE_PATH" "$METADATA_PIPE"; do
    if [ ! -p "$p" ]; then
        rm -f "$p"
        mkfifo "$p"
    fi
    chmod 777 "$p"
done

mkdir -p "$CACHE_DIR"

librespot \
    --name "$DEVICE_NAME" \
    --backend pipe \
    --device "$PIPE_PATH" \
    --format S16 \
    --bitrate "$BITRATE" \
    --initial-volume "$INITIAL_VOLUME" \
    --zeroconf-port "$ZEROCONF_PORT" \
    --cache "$CACHE_DIR" \
    --disable-audio-cache \
    --onevent /onevent.sh \
    $LIBRESPOT_EXTRA_ARGS &
LIBRESPOT_PID=$!

# librespot can wedge with its process alive but its Spotify session dead, in
# which case it never recovers on its own. The zeroconf HTTP endpoint doubles
# as a liveness probe: on sustained failure, kill librespot so the container
# exits and docker's restart policy brings it back fresh. TERM first, KILL
# after a grace period because a wedged process may never handle TERM.
(
    fails=0
    while kill -0 "$LIBRESPOT_PID" 2>/dev/null; do
        sleep "$WATCHDOG_INTERVAL"
        if curl --connect-timeout 5 --max-time 8 --silent --fail \
                "http://localhost:${ZEROCONF_PORT}/?action=getInfo" >/dev/null; then
            fails=0
        else
            fails=$((fails + 1))
            echo "watchdog: getInfo probe failed (${fails}/${WATCHDOG_FAILURES})"
            if [ "$fails" -ge "$WATCHDOG_FAILURES" ]; then
                echo "watchdog: librespot unresponsive, terminating"
                kill -TERM "$LIBRESPOT_PID" 2>/dev/null
                sleep 10
                kill -KILL "$LIBRESPOT_PID" 2>/dev/null
                break
            fi
        fi
    done
) &

wait "$LIBRESPOT_PID"
EXIT_CODE=$?
echo "librespot exited with code ${EXIT_CODE}"
exit "$EXIT_CODE"
