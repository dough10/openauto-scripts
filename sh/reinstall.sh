#!/bin/bash

bash ~/.openauto-scripts/uninstall.sh
cd ~/
curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh
bash install.sh
rm install.sh