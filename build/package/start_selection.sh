#!/usr/bin/env bash
set -eu
DIR="${HOME}/.local/share/keyman/aksharam_glyphkey"
exec /usr/bin/python3 "$DIR/aksharam_host_controls.py" watch
