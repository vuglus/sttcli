param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "Processing file"
Write-Host "Args: $Args"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FileExt = [IO.Path]::GetExtension($FilePath).ToLower()

Set-Location $ScriptDir

Write-Host "Script directory: $ScriptDir"
Write-Host "File path: $FilePath"

# Activate virtual environment
$activatePath = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    Write-Host "Activating virtual environment..."
    . $activatePath
} else {
    Write-Host "Error: Cannot find virtual environment: $activatePath"
    exit 1
}

# Extra arguments for the Python script
$extra = $Args

switch ($FileExt) {
    ".md"    { python "$ScriptDir\pipcli.py" "$FilePath" @extra }
    ".txt"   { python "$ScriptDir\pipcli.py" "$FilePath" @extra }
    ".xml"   { python "$ScriptDir\pipcli.py" "$FilePath" @extra }
    ".mp3"   { python "$ScriptDir\sttcli.py" "$FilePath" @extra }
    ".jsonl" { python "$ScriptDir\cli_parser_test.py" "$FilePath" @extra }

    default {
        Write-Host "Unsupported file extension: $FileExt"
        Write-Host "Supported extensions are .mp3, .txt, .xml and .jsonl"
    }
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
