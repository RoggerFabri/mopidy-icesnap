#!/usr/bin/dumb-init /bin/sh

env

set -x

mopidy --config /mopidy/mopidy.conf
