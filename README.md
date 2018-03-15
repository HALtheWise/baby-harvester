# BabyHarvesterHack

You will need to install gpiozero manually:
```shell
$ sudo apt install python3-gpiozero
```

Also disable the Raspbian screensaver like [this](https://www.raspberrypi.org/forums/viewtopic.php?t=57552). E.G. add the following lines to `/etc/xdg/lxsession/LXDE-pi/autostart`:
```shell
@xset s noblank 
@xset s off 
@xset -dpms

```
And set the script to run when the DE starts by appending the following to `/home/pi/.config/lxsession/LXDE-pi/autostart`:
```
@source /home/pi/baby-harvester/env.local
@python3 /home/pi/baby-harvester/test.py
```

