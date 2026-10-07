#!/usr/bin/env bash
set -euo pipefail
DIR="${HOME}/.local/share/keyman/aksharam_glyphkey"
exec xbindkeys -n -f "$DIR/xbindkeys.aksharam"
