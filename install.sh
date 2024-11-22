#!/bin/bash
set -e
version="1.3"

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

echo -e "${ORANGE} _____    ______   _    _   ______   _    _  10${NC}";
echo -e "${ORANGE}| | \ \  / |  | \ | |  | | | | ____ | |  | |   ${NC}";
echo -e "${ORANGE}| | | |  | |  | | | |  | | | |  | | | |--| |   ${NC}";
echo -e "${ORANGE}|_|_/_/  \_|__|_/ \_|__|_| |_|__|_| |_|  |_|   ${NC}";
echo -e "${WHITE}Openauto Script Installer v${NC}${GREEN}${version}${NC}";
echo -e ""
echo -e "${YELLOW}Install Dependencies${NC}"
sudo apt-get update && sudo apt-get install git xterm python3 python3-pip -y
PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1-2)
PYTHON_VENV_PACKAGE="python${PYTHON_VERSION}-venv"
if ! sudo apt install "$PYTHON_VENV_PACKAGE" -y; then
  echo -e "${RED}Warning: ${PYTHON_VENV_PACKAGE} installation failed. Attempting to continue...${NC}"
fi
echo -e "${YELLOW}Dependencies Installed${NC}"

echo -e "${YELLOW}Clone Github repo${NC}"
cd ~/
git clone -b dashcam https://github.com/dough10/openauto-scripts
echo -e "${YELLOW}Github repo cloned${NC}"

echo -e "${YELLOW}Setup virtual environment${NC}"
python3 -m venv ~/openauto-scripts/.venv
echo -e "${YELLOW}virtual environment ~/openauto-scripts/.venv created${NC}"

echo -e "${YELLOW}Installing requirments.txt${NC}"
~/openauto-scripts/.venv/bin/python3 -m pip install -r ~/openauto-scripts/requirments.txt
echo -e "${YELLOW}requirments.txt installed${NC}"

echo -e "${YELLOW}Creating autostart folder${NC}"
createFolder "~/.config/autostart"

echo -e "${YELLOW}Installing autostart shortcuts${NC}"
cp -u -p -v ~/openauto-scripts/shortcuts/*.desktop ~/.config/autostart

chmod +x ~/openauto-scripts/*.sh

sudo ln -s ~/openauto-scripts/purge_recordings.sh /usr/local/bin/purge_recordings 

chmod +x ~/.config/autostart/*.desktop

echo -e "${YELLOW}Install complete${NC}"