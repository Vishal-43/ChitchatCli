echo "Welcome to Chitchat by legends!"
echo "What do you want to do?"
echo "1. Host a server"
echo "2. Join a server"
echo "3. Exit"


read -p "Enter your choice (1-3): " choice

case "$choice" in
    1)
        echo "Hosting a server..."
        python3 start.py
        ;;
    2)
        echo "Joining a server..."
        python3 start2.py
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac
