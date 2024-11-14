# openauto-scripts

python3 scripts for openauto pro. watch GPIO pins and perform actions when states change (shutdown), adjust fan speed based on CPU temp, reset volume to lower level on shutdown (using F7, F8, F12 keybinds), remote turn on wire (for amp's, processors)  

## Install

`cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## Environment configuration

environment config is only needed if you need to change the GPIO configuration or log level and only changed values need to be added  

`nano ~/openauto-scripts/.env` to create or edit the environment config file.  

### GPIO configuration defaults

`IGN_PIN=17`  
`REMOTE_PIN=25`  
`FAN_PIN=12`  
`LATCH_PIN=4`  
`FAN_SPEED_PIN=24`

GPIO pin configuration use `GPIO.BCM` numbering standard  
<img src='https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg' alt='GPIO header' height='400px' width='400px'>

## Logging

logs are saved to users home directory. *(**openauto-scripts.log**)* Default logging level can be changed in the environment config file

### default value

`LOG_LEVEL=WARNING`

Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

to view log stream `tail -f ~/openauto-scripts.log`

## reinstall

`bash ~/openauto-scripts/uninstall.sh cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## uninstall

`bash ~/openauto-scripts/uninstall.sh`
