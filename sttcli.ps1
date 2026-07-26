# Convert audio to text

param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(Mandatory = $false)]
    [string]$Output,

    [Parameter(Mandatory = $false)]
    [switch]$ForceQuit,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING="utf-8"

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
                Write-Host "Press any key to continue..."
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                exit 1
            }
        } else {
            Write-Host "MP3 file is already mono" -ForegroundColor Green
        }
    } catch {
        Write-Host "Warning: Could not verify MP3 channels. Proceeding with original file." -ForegroundColor Yellow
        Write-Host "Press any key to continue..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Activate virtual environment
$activatePath = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    Write-Host "Activating virtual environment..."
    . $activatePath
} else {
    Write-Host "Error: Cannot find virtual environment: $activatePath"
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Determine output file path
$OutputFile = $Output
if (-not $OutputFile) {
    # Generate timestamp in DD-MM-YY-HH-MM-SS format
    $timestamp = Get-Date -Format "dd-MM-yy-HH-mm-ss"
    $base = [System.IO.Path]::GetFileNameWithoutExtension($FilePath)
    $baseDir = Split-Path $FilePath
    
    # Set default output file based on input file extension
    switch ($FileExt) {
        ".mp3"   { $OutputFile = "$baseDir/${base}_${timestamp}.txt" }
        ".md"    { $OutputFile = "$baseDir/${base}_${timestamp}.md" }
        ".txt"   { $OutputFile = "$baseDir/${base}_${timestamp}.txt" }
        ".xml"   { $OutputFile = "$baseDir/${base}_${timestamp}.xml" }
        default {
            Write-Host "Unsupported file extension: $FileExt"
            Write-Host "Supported extensions are .mp3, .txt, .xml and .jsonl"
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    }
}

# Process file based on extension
switch ($FileExt) {
    {($_ -eq ".md") -or ($_ -eq ".txt") -or ($_ -eq ".xml")} {
        # Pass -output parameter to pipcli.py
        $pipArgs = @($RemainingArgs) + "--output", "$OutputFile"
        python "$ScriptDir\pipcli.py" "$FilePath" @pipArgs
        break
    }
    ".mp3"   {
        # Create diarization file path
        $base = [System.IO.Path]::GetFileNameWithoutExtension($FilePath)
        $folder = Split-Path $FilePath
        $diaFile = Join-Path $folder "$base.dia"
        
        # Run diarization script through WSL in background
        Write-Host "Starting diarization processing through WSL in background..." -ForegroundColor Yellow
        $job = Start-Job -ScriptBlock {
            param($mp3File, $diaFile)
            & wsl -e bash "/mnt/d/Work/dia/run_diarization.sh" "$mp3File" "$diaFile"
        } -ArgumentList $FilePath, $diaFile
        
        # Pass -output parameter to sttcli.py
        $sttArgs = @($RemainingArgs) + "--output", "$OutputFile"
        python "$ScriptDir\sttcli.py" "$FilePath" @sttArgs

        # Create backup of raw STT result before diamix merge
        $backupFile = "$OutputFile.bak"
        Copy-Item "$OutputFile" "$backupFile" -Force
        Write-Host "Backup of raw STT transcript saved: $backupFile" -ForegroundColor Green
        
        # Wait for diarization job to complete
        Write-Host "Waiting for diarization job to complete..." -ForegroundColor Yellow
        Wait-Job $job
        
        # Run diamix script to combine diarization and STT results
        Write-Host "Running diamix script..." -ForegroundColor Yellow
        & D:\Work\dia\run_diamix.ps1 -TxtFile "$OutputFile" -DiaFile "$diaFile"
        break
    }
    default {
        Write-Host "Unsupported file extension: $FileExt"
        Write-Host "Supported extensions are .mp3, .txt, .xml and .jsonl"
        break
    }
}

if ( -not $ForceQuit) {
    Write-Host ""
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
