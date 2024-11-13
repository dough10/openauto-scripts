# openauto-scripts

## Install

`cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## configure GPIO pins

`nano ~/openauto-scripts/.env` to create the environment config file

### default values

`IGN_PIN=17`<br>
`REMOTE_PIN=25`<br>
`FAN_PIN=12`<br>
`LATCH_PIN=4`<br>
`FAN_SPEED_PIN=24`

environment config is only needed if you need to change a pin configuration and only the changed values need to be added to .env file

## reinstall

`bash ~/openauto-scripts/uninstall.sh cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## uninstall

`bash ~/openauto-scripts/uninstall.sh`
