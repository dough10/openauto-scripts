#!/bin/bash
version="1.0"

BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREY='\033[0;37m'
YELLOW='\033[1;33m'
WHITE='\033[1;37m'
NC='\033[0m'

checkFolder () {
  if [ -d "$1" ]
  then
    echo -e "Directory ${GREEN}$1${NC} exists."
  else
    echo -e "Creating ${GREEN}$1${NC} folder"
    mkdir $1
  fi 
}

echo "${PURPLE} _____    ______   _    _   ______   _    _  10${NC}";
echo "${PURPLE}| | \ \  / |  | \ | |  | | | | ____ | |  | |   ${NC}";
echo "${PURPLE}| | | |  | |  | | | |  | | | |  | | | |--| |   ${NC}";
echo "${PURPLE}|_|_/_/  \_|__|_/ \_|__|_| |_|__|_| |_|  |_|   ${NC}";
echo "${WHITE}Openauto Script Installer v${NC}${GREEN}${version}${NC}";
echo "${PURPLE}                                               ${NC}";

echo "${YELLOW}Updating app cache${NC}"
sudo apt-get update

echo "${YELLOW}Installing PIP${NC}"
sudo apt-get install python-pip

echo "${YELLOW}Installing pynput${NC}"
python -m pip install pynput

echo "${YELLOW}Checking for autostart folder${NC}"
checkFolder "/home/pi/.config/autostart"

echo "${YELLOW}Installing / Updating Python scripts${NC}"
cp -u -p -v power.py /home/pi
cp -u -p -v vol.py /home/pi

echo "${YELLOW}Installing / Updating autostart shortcuts${NC}"
cp -u -p -v vol.desktop /home/pi/.config/autostart
cp -u -p -v power.desktop /home/pi/.config/autostart