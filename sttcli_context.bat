@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "FILE_PATH=%~1"
set "FILE_EXT=%~x1"

cd /d %SCRIPT_DIR%
echo Текущая директория: %CD%
echo Обработка файла: %FILE_PATH%

call "%SCRIPT_DIR%sttcli\Scripts\activate.bat"

if "%FILE_EXT%"==".txt" (
    echo Запуск обработки TXT файла...
    python "%SCRIPT_DIR%cli_summarize.py" "%FILE_PATH%"
    pause
) else if "%FILE_EXT%"==".xml" (
    echo Запуск обработки XML файла...
    python "%SCRIPT_DIR%cli_summarize.py" "%FILE_PATH%"
    pause
) else if "%FILE_EXT%"==".mp3" (
    echo Запуск обработки MP3 файла...
    python "%SCRIPT_DIR%sttcli.py" "%FILE_PATH%"
    pause
) else if "%FILE_EXT%"==".jsonl" (
    echo Запуск обработки JSONL файла...
    python "%SCRIPT_DIR%cli_parser_test.py" "%FILE_PATH%"
    pause
) else (
    echo Неподдерживаемый формат файла: %FILE_EXT%
    echo Поддерживаются только .mp3 и .jsonl файлы
    pause
)

endlocal
