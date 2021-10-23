#!/bin/bash

# Copy config if it does not already exist
if [ ! -f /mopidy/mopidy.conf ]; then
    cp /mopidy_default.conf /mopidy/mopidy.conf
fi

exec mopidy --config /mopidy/mopidy.conf