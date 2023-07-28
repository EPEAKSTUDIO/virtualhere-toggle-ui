#!/bin/bash

# Function to display status messages
function display_status() {
  echo "-------------------------------------"
  echo "$1"
  echo "-------------------------------------"
}

# Function to check if a command was successful
function check_command() {
  if [ $? -eq 0 ]; then
    echo "✔️  Success"
  else
    echo "❌  Failed"
    exit 1
  fi
}

# Display header
display_status "VirtualHere Toggle UI - Installation"

# Install Python and Tkinter
display_status "Installing Python and Tkinter..."
sudo apt update
sudo apt install -y python3 python3-tk
check_command

# Download the Python script from your GitHub repository
display_status "Downloading Python script..."
wget -O /tmp/virtualhere_service_gui.py https://raw.githubusercontent.com/EPEAKSTUDIO/virtualhere-toggle-ui/main/virtualhere_service_gui.py
check_command

# Configure the script to start on boot
display_status "Configuring autostart..."
cat <<EOF | sudo tee ~/.config/autostart/virtualhere_service_gui.desktop > /dev/null
[Desktop Entry]
Name=VirtualHere Service GUI
Type=Application
Exec=/usr/bin/python3 /tmp/virtualhere_service_gui.py
EOF
check_command

# Make the script executable
display_status "Making the script executable..."
chmod +x /tmp/virtualhere_service_gui.py
check_command

# Installation completed
echo "-------------------------------------"
echo "VirtualHere Toggle UI is now installed!"
echo "A reboot is required for the changes to take effect."
echo "After reboot, the GUI will automatically start on boot."
echo "Enjoy using the VirtualHere Toggle UI!"
echo "-------------------------------------"

# Prompt for reboot
read -p "Do you want to restart your Raspberry Pi now? (Y/N): " choice
if [[ $choice =~ ^[Yy]$ ]]; then
  sudo reboot
else
  echo "You can manually reboot your Raspberry Pi to start the VirtualHere Toggle UI."
fi
