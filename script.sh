#!/bin/bash

projectName=$1

logger() {
    python3 logger.py "$1" "$2"
}


setup_venv() {
    # Create the virtual environment
    if python3 -m venv "venv_$projectName"; then
        echo "Virtual environment created successfully."
    else
        echo "Failed to create the virtual environment."
        exit 1
    fi
    
    # Activate the virtual environment
    if source "venv_$projectName/bin/activate"; then
        activated=true
        echo "Virtual environment activated successfully."
    else
        echo "Failed to activate the virtual environment 'venv_$projectName'."
        exit 1
    fi
    
    # Create the environment file
    if touch .env; then
        echo "Environment file created successfully."
    else
        echo "Failed to create the environment file."
        exit 1
    fi
    
    # Install the latest version of pip
    if pip3 install --upgrade pip -q; then
        echo "Pip upgraded successfully."
    else
        echo "Failed to upgrade pip."
    fi
    
    # Install the dependencies
    if pip3 install -r requirements.txt -q; then
        logger "info" "Dependencies installed successfully."
    else
        echo "Failed to install dependencies."
        exit 1
    fi
}



setup_venv


# Check if the Django project was created successfully
if django-admin startproject root .; then
    logger "info" "Django project created successfully."
else
    logger "error" "Failed to create the Django project."
    #exit 1
fi


# Run the main script
python3 script.py root/settings.py mysql $projectName

# Deactivate the virtual environment
if [ "$activated" = true ]; then
    deactivate
fi

