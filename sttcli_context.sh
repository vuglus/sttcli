#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE_PATH="$1"
FILE_EXT="${FILE_PATH##*.}"
$env:SPEECHBRAIN_STRATEGY = "COPY"

echo "Обработка файла: $FILE_PATH"

# Активация виртуального окружения
source "$SCRIPT_DIR/sttcli/bin/activate"

if [ "$FILE_EXT" = "mp3" ]; then
    echo "Запуск обработки MP3 файла..."
    python "$SCRIPT_DIR/sttcli.py" "$FILE_PATH"
elif [ "$FILE_EXT" = "jsonl" ]; then
    echo "Запуск обработки JSONL файла..."
    python "$SCRIPT_DIR/test_parser.py" "$FILE_PATH"
else
    echo "Неподдерживаемый формат файла: $FILE_EXT"
    echo "Поддерживаются только .mp3 и .jsonl файлы"
    read -p "Нажмите Enter для продолжения..."
fi

# Деактивация виртуального окружения
deactivate