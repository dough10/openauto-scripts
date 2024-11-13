# openauto-scripts

## Install

`cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## configure GPIO pins

`nano ~/openauto-scripts/.env` to create the enviroment config file

IGN_PIN=17
REMOTE_PIN=25
FAN_PIN=12
LATCH_PIN=4
FAN_SPEED_PIN=24

you only need the enviroment config if you need to change a pin configuration
