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

# Create the autostart directory if it doesn't exist
mkdir -p ~/.config/autostart

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

# Configure the script to start on boot using systemd
display_status "Configuring systemd service..."
sudo tee /etc/systemd/system/virtualhere_toggle_ui.service > /dev/null << EOF
[Unit]
Description=VirtualHere Toggle UI
After=network.target

[Service]
ExecStart=/usr/bin/python3 /tmp/virtualhere_service_gui.py
WorkingDirectory=/tmp
StandardOutput=null

[Install]
WantedBy=multi-user.target
EOF
check_command

# Enable the service
display_status "Enabling the VirtualHere Toggle UI service..."
sudo systemctl enable virtualhere_toggle_ui.service
check_command

# Start the service
display_status "Starting the VirtualHere Toggle UI service..."
sudo systemctl start virtualhere_toggle_ui.service
check_command

# Installation completed
echo "-------------------------------------"
echo "VirtualHere Toggle UI is now installed and running as a system service!"
echo "The GUI will automatically start on boot."
echo "Enjoy using the VirtualHere Toggle UI!"
echo "-------------------------------------"

# Prompt for reboot
read -p "Do you want to restart your Raspberry Pi now? (Y/N): " choice
if [[ $choice =~ ^[Yy]$ ]]; then
  sudo reboot
else
  echo "You can manually reboot your Raspberry Pi to start the VirtualHere Toggle UI."
fi
