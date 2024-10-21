#!/bin/bash
set -e
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

createFolder () {
  folderPath="${1/#\~/$HOME}"
  if [ -d "$folderPath" ]
  then
    echo -e "Directory ${GREEN}$folderPath${NC} exists."
  else
    echo -e "Creating ${GREEN}$folderPath${NC} folder"
    mkdir -p "$folderPath"
  fi 
}

echo -e "${PURPLE} _____    ______   _    _   ______   _    _  10${NC}";
echo -e "${PURPLE}| | \ \  / |  | \ | |  | | | | ____ | |  | |   ${NC}";
echo -e "${PURPLE}| | | |  | |  | | | |  | | | |  | | | |--| |   ${NC}";
echo -e "${PURPLE}|_|_/_/  \_|__|_/ \_|__|_| |_|__|_| |_|  |_|   ${NC}";
echo -e "${WHITE}Openauto Script Installer v${NC}${GREEN}${version}${NC}";
echo -e ""

echo -e "${YELLOW}Install Dependencies${NC}"
sudo apt-get update && sudo apt install git xterm python3 python3-pip -y
PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1-2)
PYTHON_VENV_PACKAGE="python${PYTHON_VERSION}-venv"
if ! sudo apt install "$PYTHON_VENV_PACKAGE" -y; then
  echo -e "${RED}Warning: ${PYTHON_VENV_PACKAGE} installation failed. Attempting to continue...${NC}"
fi
echo -e "${YELLOW}Dependencies Installed${NC}"

echo -e "${YELLOW}Clone Github repo${NC}"
git clone https://github.com/dough10/openauto-scripts
echo -e "${YELLOW}Github repo cloned${NC}"

echo -e "${YELLOW}Setup virtual enviroment${NC}"
python3 -m venv ~/openauto-scripts/.venv
echo -e "${YELLOW}virtual enviroment ~/openauto-scripts/.venv created${NC}"

echo -e "${YELLOW}Installing pynput${NC}"
~/openauto-scripts/.venv/bin/python3 -m pip install -r ~/openauto-scripts/requirments.txt
echo -e "${YELLOW}pynput installed${NC}"

echo -e "${YELLOW}Creating autostart folder${NC}"
createFolder "~/.config/autostart"

echo -e "${YELLOW}Installing autostart shortcuts${NC}"
cp -u -p -v ~/openauto-scripts/power.desktop ~/.config/autostart
cp -u -p -v ~/openauto-scripts/vol.desktop ~/.config/autostart

chmod +x ~/.config/autostart/vol.desktop
chmod +x ~/.config/autostart/power.desktop


echo -e "${YELLOW}Install complete${NC}"