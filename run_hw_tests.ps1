# MikroTik Hardware Validation Test Runner
# Automatically activates venv and loads environment variables

param(
    [string]$Category = "",
    [switch]$Verbose,
    [string]$Report = ""
)

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Load environment variables from .env.test
$env_content = Get-Content .env.test
foreach ($line in $env_content) { 
    if ($line -match '^([^=]+)=(.+)$') { 
        Set-Item -Path "env:$($matches[1])" -Value $matches[2]
    } 
}

# Build command
$cmd = "python tests/hardware_validation.py"

if ($Category) {
    $cmd += " --category $Category"
}

if ($Verbose) {
    $cmd += " -v"
}

if ($Report) {
    $cmd += " --report $Report"
}

# Run tests
Write-Host "Running: $cmd" -ForegroundColor Cyan
Invoke-Expression $cmd

