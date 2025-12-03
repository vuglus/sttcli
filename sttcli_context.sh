#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE_PATH="$1"
FILE_EXT="${FILE_PATH##*.}"
$env:SPEECHBRAIN_STRATEGY = "COPY"

echo "Processing file: $FILE_PATH"

# Activate virtual environment
source "$SCRIPT_DIR/sttcli/bin/activate"

if [ "$FILE_EXT" = "mp3" ]; then
    echo "Starting MP3 file processing..."
    python "$SCRIPT_DIR/sttcli.py" "$FILE_PATH"
else
    echo "Unsupported file format: $FILE_EXT"
    echo "Only .mp3 and .jsonl files are supported"
    read -p "Press Enter to continue..."
fi

# Deactivate virtual environment
deactivate