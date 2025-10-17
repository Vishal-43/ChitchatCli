Write-Host "Starting ChitchatCli setup..."
Write-Host "Made by legend"
Write-Host "Visit github.com/Vishal-43 for more projects"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Installing Git via Chocolatey..."
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Host "Chocolatey not found. Installing Chocolatey first..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    }
    choco install git -y
} else {
    Write-Host "Git is already installed."
}


$RepoURL = "https://github.com/Vishal-43/ChitchatCli.git"
$InstallDir = "$env:USERPROFILE\chitchat"

if (Test-Path $InstallDir) {
    Write-Host "Repository already exists. Pulling latest changes..."
    Set-Location $InstallDir
    git pull
} else {
    Write-Host "Cloning repository..."
    git clone $RepoURL $InstallDir
}


$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not $CurrentPath.Split(";") -contains $InstallDir) {
    Write-Host "Adding chitchat folder to PATH..."
    [Environment]::SetEnvironmentVariable("PATH", "$CurrentPath;$InstallDir", "User")
    Write-Host "PATH updated. You may need to restart your terminal to use 'chitchat'."
} else {
    Write-Host "chitchat is already in PATH."
}

Write-Host "Installation complete! You can now run 'chitchat' from any terminal."
