#!/bin/bash
set -e
echo "remove ~/fan_curves folder? (y,n)"
read -r response
if [ "$response" == "y" ] || [ "$response" == "Y" ]; then
  rm -rfv ~/fan_curves
fi
rm -rf ~/.openauto-scripts
rm -fv ~/.config/autostart/oas*.desktop
rm -fv ~/openauto-scripts.log
sudo rm -fv /usr/local/bin/oas_*