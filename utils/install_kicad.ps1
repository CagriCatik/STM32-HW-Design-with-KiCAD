# Check the current execution policy
$currentPolicy = Get-ExecutionPolicy

# If the policy is restricted, temporarily bypass it
if ($currentPolicy -eq "Restricted") {
    Write-Host "Execution policy is Restricted. Temporarily bypassing the restriction for this session..."
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
}

# Set the URL for the KiCad installer
$installerUrl = "https://github.com/KiCad/kicad-source-mirror/releases/download/8.0.5/kicad-8.0.5-x86_64.exe"

# Set the output path for the installer
$installerPath = "$env:TEMP\kicad-8.0.5-x86_64.exe"

# Download the KiCad installer
Write-Host "Downloading KiCad installer..."
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

# Check if the installer was downloaded successfully
if (Test-Path $installerPath) {
    Write-Host "Download complete. Running installer..."
    
    # Run the installer silently
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
    
    Write-Host "KiCad installation completed."
} else {
    Write-Host "Failed to download the installer. Please check the URL or network connection."
}

# Restore the original execution policy (optional)
Write-Host "Restoring original execution policy: $currentPolicy"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy $currentPolicy -Force
