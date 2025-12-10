param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(Mandatory = $false)]
    [string]$Output,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FileExt = [IO.Path]::GetExtension($FilePath).ToLower()

Set-Location $ScriptDir

# Check if MP3 is mono for MP3 files
if ($FileExt -eq ".mp3") {
    try {
        $ffprobeOutput = & ffprobe -v quiet -print_format json -show_streams "$FilePath" 2>$null
        $ffprobeJson = $ffprobeOutput | ConvertFrom-Json
        $channels = $ffprobeJson.streams | Where-Object { $_.codec_type -eq "audio" } | Select-Object -ExpandProperty channels -First 1
        
        if ($channels -ne 1) {
            Write-Host "Warning: MP3 file is not mono ($channels channels). Converting to mono..." -ForegroundColor Yellow
            $tempFile = [System.IO.Path]::GetTempFileName() + ".mp3"
            & ffmpeg -i "$FilePath" -ac 1 "$tempFile" -y 2>$null
            if ($LASTEXITCODE -eq 0) {
                $FilePath = $tempFile
                Write-Host "Converted to mono MP3: $FilePath" -ForegroundColor Green
            } else {
                Write-Host "Error: Failed to convert MP3 to mono" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "MP3 file is already mono" -ForegroundColor Green
        }
    } catch {
        Write-Host "Warning: Could not verify MP3 channels. Proceeding with original file." -ForegroundColor Yellow
    }
}

# Activate virtual environment
$activatePath = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    Write-Host "Activating virtual environment..."
    . $activatePath
} else {
    Write-Host "Error: Cannot find virtual environment: $activatePath"
    exit 1
}

# Process --output parameter
if ($Output) {
    # Redirect output to the specified file
    switch ($FileExt) {
        ".md"    { python "$ScriptDir\pipcli.py" "$FilePath" @Args > "$Output" 2>&1 }
        ".txt"   { python "$ScriptDir\pipcli.py" "$FilePath" @Args > "$Output" 2>&1 }
        ".xml"   { python "$ScriptDir\pipcli.py" "$FilePath" @Args > "$Output" 2>&1 }
        ".mp3"   { python "$ScriptDir\sttcli.py" "$FilePath" @Args > "$Output" 2>&1 }
        
        default {
            Write-Host "Unsupported file extension: $FileExt"
            Write-Host "Supported extensions are .mp3, .txt, .xml and .jsonl"
            exit 1
        }
    }
} else {
    # No output file specified, run normally
    switch ($FileExt) {
        ".md"    { python "$ScriptDir\pipcli.py" "$FilePath" @Args }
        ".txt"   { python "$ScriptDir\pipcli.py" "$FilePath" @Args }
        ".xml"   { python "$ScriptDir\pipcli.py" "$FilePath" @Args }
        ".mp3"   { python "$ScriptDir\sttcli.py" "$FilePath" @Args }
        
        default {
            Write-Host "Unsupported file extension: $FileExt"
            Write-Host "Supported extensions are .mp3, .txt, .xml and .jsonl"
            exit 1
        }
    }
}
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
