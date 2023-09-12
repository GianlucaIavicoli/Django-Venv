#!/bin/bash

projectName=$1

setup_venv() {
    # Create the virtual environment
    python3 -m venv "venv_$projectName"
    
    # Activate the virtual environment
    if source "venv_$projectName/bin/activate"; then
        activated=true
    else
        echo "Failed to activate the virtual environment 'venv_$projectName'."
        exit 1
    fi
    
    #touch .env
    
    #pip install --upgrade pip
    #pip3 install -r requirements.txt
}


setup_venv

django-admin startproject root .

python3 script.py root/settings.py mysql $projectName

if [ "$activated" = true ]; then
    deactivate
fi

