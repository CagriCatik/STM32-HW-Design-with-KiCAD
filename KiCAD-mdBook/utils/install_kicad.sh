#!/bin/bash

# KiCad Installation Script

# Function to display installation progress
display_progress() {
    echo "Installing KiCad..."
}

# Function to install KiCad
install_kicad() {
    display_progress
    # Add KiCad PPA repository
    sudo add-apt-repository --yes ppa:kicad/kicad-5.1-releases
    # Update package lists
    sudo apt-get update
    # Install KiCad
    sudo apt-get install --yes kicad
}

# Main function
main() {
    install_kicad
    echo "KiCad installation complete."
}

# Execute main function
main
