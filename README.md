# openauto-scripts

python3 scripts for openauto pro. watch GPIO pins and perform actions when states change (shutdown), adjust fan speed based on CPU temp, reset volume to lower level on shutdown (using F7, F8, F12 keybinds), remote turn on wire (for amp's, processors)  

## Install

`cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/dashcam/install.sh && bash install.sh && rm install.sh`

## Environment configuration

environment config is used if you need to change the GPIO configuration, log level, dashcam recording location or time till shutdown. Only changed values need to be added  

`nano ~/openauto-scripts/.env` to create or edit the environment config file.  

### GPIO configuration defaults

`IGN_PIN=17` - HIGH if the ignigtion is on LOW when off  
`LATCH_PIN=4` - relay control  
`REMOTE_PIN=25` - remote turn on  
`FAN_PIN=12` - fan PWM pin  
`FAN_SPEED_PIN=24` - fan Tach pin

GPIO pin configuration use `GPIO.BCM` numbering standard  
<img src='https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg' alt='GPIO header' height='400px' width='400px'>

### Shutdown timer

`IGN_LOW_TIME=3` time in seconds to delay before shutdown initiated after ignition is turned off  

### Dashcam recording

`REC_LOC=~/Videos` folder location to store dashcam recordings

### Logging

`LOG_LEVEL=WARNING`

logs are saved to users home directory. *(**openauto-scripts.log**)*

Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

to view log stream `tail -f ~/openauto-scripts.log`

## Uninstall & Reinstall

`bash ~/openauto-scripts/uninstall.sh cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/dashcam/install.sh && bash install.sh && rm install.sh`

## Uninstall

`bash ~/openauto-scripts/uninstall.sh`
