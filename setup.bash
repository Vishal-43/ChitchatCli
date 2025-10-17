echo "Starting ChitchatCli setup..."
echo "made by legend"
echo "visit github.com/Vishal-43 for more projects"

if ! command -v git &> /dev/null
then
    echo "Git not found. Installing git..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y git
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install git
    else
        echo "Unsupported OS. Please install git manually."
        exit 1
    fi
else
    echo "Git is already installed."
fi

REPO_URL="https://github.com/Vishal-43/ChitchatCli"
INSTALL_DIR="$HOME/chitchat"

if [ -d "$INSTALL_DIR" ]; then
    echo "Repository already exists in $INSTALL_DIR. Pulling latest changes..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

SHELL_RC="$HOME/.bashrc" 
if ! grep -q 'chitchat' "$SHELL_RC"; then
    echo "Adding chitchat to PATH..."
    echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_RC"
    echo "PATH updated. Reloading shell..."
    source "$SHELL_RC"
else
    echo "chitchat is already in PATH."
fi

echo "Installation complete! You can now run 'chitchat' from anywhere."
