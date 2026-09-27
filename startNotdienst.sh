#!/bin/bash

cd ~/dev/notdienst
source ./.venv/bin/activate

# Regenerate the duty page every 15 minutes in the background.
(
    while true; do
        python notdienst.py
        sleep 900
    done
) &

# Serve ONLY the generated output directory. The old command served the
# whole project root - including .env with the API credentials - to the
# network, and blocked forever so the refresh loop above never ran.
exec python -m http.server -d data -b 0.0.0.0 8080
