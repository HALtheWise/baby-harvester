# BabyHarvesterHack

#Deployment environment
You will need to install packages manually, as pipenv is a little buggy on raspi:
```shell
$ sudo apt install python3-gpiozero python3-requests
```

Also disable the Raspbian screensaver like [this](https://www.raspberrypi.org/forums/viewtopic.php?t=57552). E.G. add the following lines to `/etc/xdg/lxsession/LXDE-pi/autostart`:
```shell
@xset s noblank 
@xset s off 
@xset -dpms
```

### run on startup
And set the script to run when the DE starts by appending the following to `/home/pi/.config/lxsession/LXDE-pi/autostart`:
```
@source /home/pi/baby-harvester/env.local
@python3 /home/pi/baby-harvester/test.py
```

### unit file
For fast testing, there's also a systemd unit file. Comment out the lines in LXDE autostart, and do the following:
```
$ sudo cp ./babyHarvest.service /lib/systemd/system/
$ sudo systectl daemon-reload
```
You may then start or stop the service via systemctl, e.g.
```
$ sudo systemctl start babyHarvest.service
```


## Local development

For dependency resolution:
```
$ pipenv install
```

Also install chromedriver.
