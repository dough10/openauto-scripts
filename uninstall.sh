#!/bin/bash
set -e
rm -rf ~/.openauto-scripts
rm -f ~/.config/autostart/oas.desktop
rm -f ~/openauto-scripts.log
sudo rm -f /usr/local/bin/purge_recordings
echo "remove ~/fan_curves folder? (y,n)"
read -r response
if [ "$response" == "y" ] || [ "$response" == "Y" ]; then
  rm -rfv ~/fan_curves
fi