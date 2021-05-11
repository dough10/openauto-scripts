#!/bin/bash
CODE='\033['
BLACK=$CODE'0;30m'
RED=$CODE'0;31m'
GREEN=$CODE'0;32m'
ORANGE=$CODE'0;33m'
BLUE=$CODE'0;34m'
PURPLE=$CODE'0;35m'
CYAN=$CODE'0;36m'
GREY=$CODE'0;37m'
YELLOW=$CODE'1;33m'
WHITE=$CODE'1;37m'
NC=$CODE'0m'

checkFolder () {
  if [ -d "$1" ]
  then
    echo -e "Directory ${GREEN}$1${NC} exists."
  else
    echo -e "Creating ${GREEN}$1${NC} folder"
    mkdir $1
  fi 
}

checkFolder "/home/pi/.config/autostart"

echo -e "${YELLOW}Copying Python scripts${NC}"
cp -u -p -v power.py /home/pi
cp -u -p -v vol.py /home/pi

echo -e "${YELLOW}Copying autostart shortcuts${NC}"
cp -u -p -v vol.desktop /home/pi/.config/autostart
cp -u -p -v power.desktop /home/pi/.config/autostart