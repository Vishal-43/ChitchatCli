# --- 1. Check for Git ---
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Installing Git via Chocolatey..."

    # Check if Chocolatey exists
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Host "Chocolatey not found. Installing Chocolatey first..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }

    # Install Git via Chocolatey
    choco install git -y
} else {
    Write-Host "Git is already installed."
}

# --- 2. Clone the repo ---
$RepoURL = "https://github.com/Vishal-43/ChitchatCli"
$InstallDir = "$env:USERPROFILE\chitchat"

if (Test-Path $InstallDir) {
    Write-Host "Repository already exists. Pulling latest changes..."
    Set-Location $InstallDir
    git pull
} else {
    Write-Host "Cloning repository..."
    git clone $RepoURL $InstallDir
}

# --- 3. Add folder to PATH ---
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Normalize paths to avoid duplicates
$Paths = $UserPath.Split(";") | ForEach-Object { $_.Trim() }
if (-not ($Paths -contains $InstallDir)) {
    Write-Host "Adding chitchat folder to PATH..."
    $NewPath = "$UserPath;$InstallDir"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "PATH updated. Please restart PowerShell to use 'chitchat'."
} else {
    Write-Host "chitchat is already in PATH."
}

Write-Host "Installation complete! You can now run 'chitchat' from any terminal."
