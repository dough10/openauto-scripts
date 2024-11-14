# openauto-scripts

## Install

`cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## Envoronment configuration

`nano ~/openauto-scripts/.env` to create or edit the environment config file.  

environment config is only needed if you need to change the GPIO configuration or log level and only changed values need to be added

### GPIO configuration defaults

`IGN_PIN=17`  
`REMOTE_PIN=25`  
`FAN_PIN=12`  
`LATCH_PIN=4`  
`FAN_SPEED_PIN=24`

## Logging

logs are saved to users home directory. *(**vol.py.log** and **power.py.log**)* Default logging level can be changed in the environment config file

### default value

`LOG_LEVEL=WARNING`

to view log stream `tail -f ~/power.py.log` or `tail -f ~/vol.py.log`

## reinstall

`bash ~/openauto-scripts/uninstall.sh cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## uninstall

`bash ~/openauto-scripts/uninstall.sh`
