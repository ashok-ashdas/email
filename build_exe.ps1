# Build the Email Scanner executable using the local virtual environment.
# Run this from the repository root in PowerShell.

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Error "Python executable not found at $python. Activate the venv or install dependencies first."
    exit 1
}

& $python -m PyInstaller --noconfirm --onefile --windowed --name EmailScanner --icon email_scanner.ico `
    --hidden-import=bs4 --hidden-import=beautifulsoup4 --collect-all=bs4 main.py

if (Test-Path "$PSScriptRoot\dist\EmailScanner.exe") {
    Write-Host "Build complete: $PSScriptRoot\dist\EmailScanner.exe"
} else {
    Write-Error "Build failed. Check PyInstaller output for details."
    exit 1
}
