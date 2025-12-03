
param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Обработка файла"
Write-Host "Доп. параметры: $Args"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FileExt = [IO.Path]::GetExtension($FilePath).ToLower()

Set-Location $ScriptDir

Write-Host "Текущая директория: $ScriptDir"
Write-Host "Обработка файла: $FilePath"

# Активация venv
$activatePath = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    Write-Host "Активация виртуального окружения..."
    . $activatePath
} else {
    Write-Host "? Не найден файл активации: $activatePath"
    exit 1
}

# Все дополнительные параметры пробрасываем как есть
$extra = $Args

switch ($FileExt) {
    ".md"    { python "$ScriptDir\cli_summarize.py" "$FilePath" @extra }
    ".txt"   { python "$ScriptDir\cli_summarize.py" "$FilePath" @extra }
    ".xml"   { python "$ScriptDir\cli_summarize.py" "$FilePath" @extra }
    ".mp3"   { python "$ScriptDir\sttcli.py" "$FilePath" @extra }
    ".jsonl" { python "$ScriptDir\cli_parser_test.py" "$FilePath" @extra }

    default {
        Write-Host "Неподдерживаемый формат файла: $FileExt"
        Write-Host "Поддерживаются только .mp3, .txt, .xml и .jsonl файлы"
    }
}

Write-Host ""
Write-Host "Нажмите любую клавишу для выхода..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
