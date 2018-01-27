#!/bin/bash

# Directory containing incoming nfsen/nfdump data
dir_nfcaps=/opt/nfsen/profiles-data/live/

# Path to script for handling nfdump data
path_script="python /opt/flow-to-if/nfdump-to-packet.py"

inotifywait -r -m "$dir_nfcaps" -e create -e moved_to --format '%w%f' |
    while IFS=' ' read -r fname
    do
        shortname=$(basename $fname)
        if [[ $shortname  = nfcapd.2* ]]; then
            [ -f "$fname" ] && echo "new file:" && echo $fname
            nohup nfdump -r $fname -q -o csv | $path_script - &>/dev/null &
        
        else
          [ -f "$fname" ] && echo "new file (NOT used):" && echo $fname
        fi
    done
