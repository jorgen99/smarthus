#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE=$SCRIPT_DIR/events_log.txt

python tellstick_events.py > $LOG_FILE
