#!/bin/bash
set -e
rm -rf ~/.openauto-scripts
rm ~/.config/autostart/oas.desktop
rm ~/openauto-scripts.log
sudo rm /usr/local/bin/purge_recordings
echo "remove ~/fan_curves folder? (y,n)"
read -r response
if [ "$response" == "y" ] || [ "$response" == "Y" ]; then
  rm -rf ~/fan_curves
fi