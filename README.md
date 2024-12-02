# openauto-scripts

Python3 scripts for OpenAuto Pro. Monitors GPIO pins and performs actions when their states change (e.g., shutdown), adjusts fan speed based on CPU temperature, resets volume to a lower level on shutdown (using F7, F8, and F12 keybinds), and remotely powers on devices (e.g., amps, processors) via a wire.  

## Install

To install, run the following command: `cd ~/ && curl -O https://raw.githubusercontent.com/dough10/openauto-scripts/refs/heads/main/install.sh && bash install.sh && rm install.sh`

## Environment configuration

The environment configuration is used to enable features, change GPIO settings, adjust log levels, specify dashcam recording location, or set the shutdown delay. Only modify the values you need to change.

To create or edit the environment configuration file: `nano ~/.openauto-scripts/.env`

### Features

`DASHCAM=false`: enables or disables dashcam recording  
`PWM=false`: enables or disables pwm fan control  
`VOL=false`: enables or disables volume monitor that restores volume to lower level on shutdown  

Set values to: *(`true`, `t`, `1`, `yes`, `y`)* to enable, or *(`false`, `f`, `0`, `no`, `n`)* to disable.  

### GPIO configuration defaults

`IGN_PIN=17`: HIGH if the ignigtion is on LOW when off  
`LATCH_PIN=4`: relay control  
`REMOTE_PIN=25`: remote turn on  
`FAN_PIN=12`: fan PWM pin  
`FAN_SPEED_PIN=24`: Fan tachometer pin

GPIO pin configuration use `GPIO.BCM` numbering standard  
<img src='https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg' alt='GPIO header' height='400px' width='400px'>

### Shutdown timer

`IGN_LOW_TIME=3`: Time in seconds to delay before shutdown is initiated after ignition is turned off.

### Dashcam recording

`REC_LOC=~/Videos`: Folder to save dashcam recordings.

### Logging

`LOG_LEVEL=WARNING`: Set the log level.

Logs are saved to the user's home directory as `openauto-scripts.log`

Log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

To view the log stream: `oas_log`

## Uninstall & Reinstall

To uninstall and reinstall the script, run the following: `oas_reinstall`  

## Uninstall

To uninstall the script, run: `oas_uninstall`
