#!/bin/bash
set -e
version="1.6"

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
    echo -e "${YELLOW}Directory ${NC}${GREEN}$folderPath${NC}${YELLOW} exists.${NC}"
  else
    echo -e "${YELLOW}Creating folder ${NC}${GREEN}$folderPath${NC}"
    mkdir -pv "$folderPath"
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
if ! sudo apt-get install "$PYTHON_VENV_PACKAGE" -y; then
  echo -e "${RED}Warning: ${NC}${GREY}${PYTHON_VENV_PACKAGE}${NC}${RED} installation failed. Attempting to continue...${NC}"
fi
echo -e "${YELLOW}Dependencies Installed${NC}"

echo -e "${YELLOW}Cloning Github repo${NC}"
cd ~/
git clone https://github.com/dough10/openauto-scripts
mv -v ~/openauto-scripts ~/.openauto-scripts
echo -e "${YELLOW}Github repo cloned and moved to ${NC}${GREEN}~/.openauto-scripts${NC}"

echo -e "${YELLOW}Setting virtual environment${NC}"
python3 -m venv ~/.openauto-scripts/.venv
echo -e "${YELLOW}virtual environment ${NC}${GREEN}~/.openauto-scripts/.venv${NC}${YELLOW} created${NC}"

echo -e "${YELLOW}Installing requirments.txt to ${NC}${GREEN}~/.openauto-scripts/.venv${NC}"
~/.openauto-scripts/.venv/bin/python3 -m pip install -r ~/.openauto-scripts/requirments.txt
echo -e "${YELLOW}requirments.txt installed${NC}"

createFolder ~/.config/autostart

echo -e "${YELLOW}Installing autostart shortcuts${NC}"
cp -upv ~/.openauto-scripts/shortcuts/*.desktop ~/.config/autostart

echo -e "${YELLOW}Adding execute permissions${NC}"
chmod +x -v ~/.openauto-scripts/*.sh
chmod +x -v ~/.openauto-scripts/sh/*.sh
chmod +x -v ~/.config/autostart/*.desktop
chmod +x -v ~/.openauto-scripts/oas.py

echo -e "${YELLOW}Installing global commands${NC}"
sudo ln -sfv ~/.openauto-scripts/uninstall.sh /usr/local/bin/oas_uninstall
sudo ln -sfv ~/.openauto-scripts/sh/reinstall.sh /usr/local/bin/oas_reinstall
sudo ln -sfv ~/.openauto-scripts/sh/purge_recordings.sh /usr/local/bin/oas_purge
sudo ln -sfv ~/.openauto-scripts/sh/tail_log.sh /usr/local/bin/oas_log

createFolder ~/fan_curves

echo -e "${YELLOW}Copying premade fan curves${NC}"
cp -nv ~/.openauto-scripts/curves/*.json ~/fan_curves

echo -e "${YELLOW}Install complete. run ${NC}${CYAN}nano ~/.openauto-scripts/.env${NC}${YELLOW} to configure environment.${NC}"
echo -e "${YELLOW}Then reboot after${NC}"