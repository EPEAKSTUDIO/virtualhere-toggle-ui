#!/bin/bash
# Script version

VERSION="v0.22"

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

# Check if running with root/sudo permissions
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)" 
   exit 1
fi

# Display version information
echo "VirtualHere Toggle UI Installer (Version: $VERSION)"

# Check if python3 and python3-tk are installed
display_status "Checking for Python 3 and Python Tkinter"
dpkg -l python3 python3-tk
check_command

# Install required packages
display_status "Installing required packages"
apt update
apt install -y python3 python3-tk
check_command

# Clone the VirtualHere Toggle UI repository
display_status "Cloning VirtualHere Toggle UI repository"
git clone https://github.com/EPEAKSTUDIO/virtualhere-toggle-ui.git /tmp/virtualhere-toggle-ui
check_command

# Copy the VirtualHere Toggle UI script to /usr/local/bin
display_status "Copying VirtualHere Toggle UI script"
cp /tmp/virtualhere-toggle-ui/virtualhere_service_gui.py /usr/local/bin/virtualhere_service_gui.py
chmod +x /usr/local/bin/virtualhere_service_gui.py
check_command

# Clean up
display_status "Cleaning up"
rm -rf /tmp/virtualhere-toggle-ui
check_command

# Create the systemd service unit file
display_status "Creating systemd service unit file"
cat > /etc/systemd/system/virtualhere-toggle-ui.service << EOL
[Unit]
Description=VirtualHere Toggle UI
After=graphical.target network.target
Wants=network.target

[Service]
User=$USER
ExecStart=/usr/bin/python3 /usr/local/bin/virtualhere_service_gui.py
Restart=on-abort
RestartSec=5  # Optional: Add a delay of 5 seconds before restarting the service

[Install]
WantedBy=graphical.target
EOL
check_command

# Enable and start the service
display_status "Enabling and starting the service"
systemctl enable virtualhere-toggle-ui.service
systemctl start virtualhere-toggle-ui.service
check_command

# Create desktop shortcut for manual launch
display_status "Creating desktop shortcut"
desktop_file="/home/$SUDO_USER/Desktop/VirtualHere_Toggle_UI.desktop"
cat > "$desktop_file" << EOL
[Desktop Entry]
Name=VirtualHere Toggle UI
Exec=/usr/bin/python3 /usr/local/bin/virtualhere_service_gui.py
Icon=/path/to/your/icon.png  # Replace this with the actual path to your icon (if you have one)
Type=Application
Terminal=false
EOL
check_command

# Set permission for the desktop shortcut
chmod +x "$desktop_file"
check_command

# Ask user if they want to reboot the system
echo "Do you want to reboot the system now? (Y/N)"
read -r answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  echo "Rebooting the system..."
  sleep 2
  reboot
else
  echo "Installation of VirtualHere Toggle UI (Version: $VERSION) completed."
  echo "The application will automatically start on the next boot, and you can also manually start it from the desktop shortcut."
fi
