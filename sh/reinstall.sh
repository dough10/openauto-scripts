#!/bin/bash

[ -f ~/.openauto-scripts/.env ] && cp -v ~/.openauto-scripts/.env ~/.oas-env
bash ~/.openauto-scripts/uninstall.sh
cd ~/
curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh
bash install.sh
rm install.sh
[ -f ~/.oas-env ] && cp -v ~/.oas-env ~/.openauto-scripts/.env
