#!/bin/bash

cd ~/dev/notdienst
# cd html
python -m http.server -d . -b 0.0.0.0 8080

# cd ..
source ./.venv/bin/activate

while true; do
    python NotdienstWeb.py
    # sleep 900 # Sleep for 5 minutes (300 seconds)
done
