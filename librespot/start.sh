#!/usr/bin/dumb-init /bin/sh

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
    --zeroconf-backend "$ZEROCONF_BACKEND" \
    --cache "$CACHE_DIR" \
    --disable-audio-cache \
    --onevent /onevent.sh \
    $LIBRESPOT_EXTRA_ARGS &
LIBRESPOT_PID=$!

# librespot can wedge with its process alive but its Spotify session dead, in
# which case it never recovers on its own. /probe.sh checks both the zeroconf
# endpoint and the cloud session: on sustained failure, kill librespot so the
# container exits and docker's restart policy brings it back fresh. TERM
# first, KILL after a grace period because a wedged process may never handle
# TERM.
#
# Two counters, because probe.sh reports two classes of failure. Exit 1 is a believed fault
# (connection refused, HTTP error, librespot process missing, cloud session gone) and trips
# after WATCHDOG_FAILURES. Exit 2 is inconclusive -- almost always a timeout on a busy host --
# and needs WATCHDOG_SOFT_FAILURES, which is deliberately much larger, so a slow box does not
# get its working librespot killed.
#
# Neither counter resets the other: alternating hard and soft failures still accumulate and
# will eventually trip, so a genuinely sick librespot cannot hide by failing inconsistently.
# Only a clean probe clears both.
(
    fails=0
    soft=0
    while kill -0 "$LIBRESPOT_PID" 2>/dev/null; do
        sleep "$WATCHDOG_INTERVAL"
        /probe.sh
        rc=$?
        case "$rc" in
            0)
                fails=0
                soft=0
                ;;
            1)
                fails=$((fails + 1))
                echo "watchdog: probe failed (${fails}/${WATCHDOG_FAILURES})"
                ;;
            *)
                soft=$((soft + 1))
                echo "watchdog: probe inconclusive (${soft}/${WATCHDOG_SOFT_FAILURES})"
                ;;
        esac
        if [ "$fails" -ge "$WATCHDOG_FAILURES" ] || [ "$soft" -ge "$WATCHDOG_SOFT_FAILURES" ]; then
            echo "watchdog: librespot unresponsive, terminating"
            kill -TERM "$LIBRESPOT_PID" 2>/dev/null
            sleep 10
            kill -KILL "$LIBRESPOT_PID" 2>/dev/null
            break
        fi
    done
) &

wait "$LIBRESPOT_PID"
EXIT_CODE=$?
echo "librespot exited with code ${EXIT_CODE}"
exit "$EXIT_CODE"
