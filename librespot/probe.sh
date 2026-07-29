#!/bin/sh

# Liveness probe for librespot, shared by the container HEALTHCHECK and the
# start.sh watchdog. Exit 0 = healthy.
#
# Check 1: the zeroconf HTTP endpoint answers (LAN discovery half).
#
# Check 2: the Spotify cloud session is alive. librespot can wedge with the
# AP connection (remote port 4070) still established but the dealer
# websocket (remote port 443) gone — it then logs nothing, never reconnects,
# and the device silently disappears from Spotify Connect while zeroconf
# still answers. A healthy session keeps the dealer websocket open at all
# times, so the sustained absence of any ESTABLISHED librespot socket with
# remote port 443 means the session is dead. The check self-arms via a
# marker file the first time such a connection is seen, so credential-less
# deployments that idle without a session are not restart-looped.

# Two failure classes, not one. curl's exit code says which:
#
#   7  connection refused  -- nothing is listening, librespot's zeroconf half is genuinely
#                             gone. Instant and unambiguous, so believe it.
#   22 HTTP error (--fail) -- it answered, badly. Also a real fault.
#   52 empty reply         -- it accepted then gave nothing. Real fault.
#   28 timed out           -- says as much about the host as about librespot. On a loaded Pi
#                             this fires because the box is slow, not because anything broke.
#
# Collapsing all of these into one `exit 1` is what let a slow host look like a broken
# service. Exit 1 is now a believed fault that start.sh acts on quickly; exit 2 is
# inconclusive and has to persist far longer before it does (WATCHDOG_SOFT_FAILURES).
# Unknown codes are treated as inconclusive on purpose -- the conservative side here is
# fewer restarts, since a needless restart of a working service is the worse outcome.
#
# Docker's HEALTHCHECK marks the container unhealthy on either, which is right: it reports
# without restarting anything.
rc=0
curl --connect-timeout 5 --max-time 8 --silent --fail \
    "http://localhost:${ZEROCONF_PORT}/?action=getInfo" >/dev/null || rc=$?

case "$rc" in
    0) ;;
    7 | 22 | 52 | 56)
        echo "probe: zeroconf endpoint not answering (curl exit ${rc})"
        exit 1
        ;;
    28)
        echo "probe: zeroconf endpoint timed out (curl exit 28) -- host may just be slow"
        exit 2
        ;;
    *)
        echo "probe: zeroconf probe inconclusive (curl exit ${rc})"
        exit 2
        ;;
esac

[ "$WATCHDOG_CLOUD_CHECK" = "off" ] && exit 0

pid=
for p in /proc/[0-9]*; do
    if [ "$(cat "$p/comm" 2>/dev/null)" = "librespot" ]; then
        pid=${p#/proc/}
        break
    fi
done
if [ -z "$pid" ]; then
    echo "probe: librespot process not found"
    exit 1
fi

# The container runs with host networking, so /proc/net/tcp* lists the whole
# host: filter to sockets whose inode belongs to the librespot process.
inodes=$(for fd in /proc/"$pid"/fd/*; do readlink "$fd"; done 2>/dev/null \
    | sed -n 's/^socket:\[\(.*\)\]$/\1/p' | tr '\n' ' ')

if awk -v inodes="$inodes" '
    BEGIN { n = split(inodes, a, " "); for (i = 1; i <= n; i++) set[a[i]] = 1 }
    FNR > 1 && $4 == "01" && ($10 in set) {
        split($3, r, ":")
        if (r[2] == "01BB") { found = 1; exit }
    }
    END { exit found ? 0 : 1 }
' /proc/net/tcp /proc/net/tcp6; then
    touch /run/librespot-cloud-armed
    exit 0
fi

if [ -f /run/librespot-cloud-armed ]; then
    echo "probe: cloud session gone (no dealer websocket)"
    exit 1
fi
exit 0
