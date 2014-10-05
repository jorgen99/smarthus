#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE=$SCRIPT_DIR/cronlog.txt

cd $SCRIPT_DIR
#sudo gunicorn -b 0.0.0.0:80 smarthus:app --daemon --pid 104711
gunicorn smarthus:app
