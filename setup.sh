#!/bin/bash

set -e
set -o pipefail

function venv() {
    echo 'Do you have virtualenv installed on your machine?'
    echo "Enter y or n"

    read response
  
    if [ $response == "y" ]; then
      echo "Do you want it activated for the project"
      echo "y or n"
  
      read answer
  
      if [ $answer == "y" ]; then
        virtualenv --python=python3 venv
        source venv/bin/activate
        echo "Your virtual environment has been activated"
      else
        echo "It seems you have development environment all setup"
      fi
    else
      echo "Do you want it to be installed an activated as well"
      echo  "y or n"

      read response
  
      if [ $response == "y" ]; then
        pip install virtualenv
        virtualenv --python=python3 venv
        source venv/bin/activate
        echo "Your virtual environment has been activated"
      else
        echo "It seems your have development environment all setup"
      fi
    fi
}

venv
