#!/bin/bash
cd "$(dirname "$0")"
PYTHON_BIN="$(command -v python3)"
if [ -z "$PYTHON_BIN" ]; then
  echo "Python 3 was not found. Install Python 3 and try again."
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
