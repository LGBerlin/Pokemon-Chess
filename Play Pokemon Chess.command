#!/bin/bash
cd "$(dirname "$0")" || exit 1
if [ -x /opt/homebrew/bin/python3.14 ]; then
  PYTHON_BIN=/opt/homebrew/bin/python3.14
else
  PYTHON_BIN="$(command -v python3)"
fi
if [ -z "$PYTHON_BIN" ]; then
  echo "Python 3 was not found."
  read -r -p "Press Enter to close..."
  exit 1
fi
"$PYTHON_BIN" pokemon_chess.py
RESULT=$?
if [ "$RESULT" -ne 0 ]; then
  echo "The game stopped with error code $RESULT."
  read -r -p "Press Enter to close..."
fi
exit "$RESULT"
