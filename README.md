# Kamstrup impulse counter using 4kbit 1-Wire RAM with Counter DS2423 on Raspbian using OWFS

## Setup

RASPBIAN JESSIE LITE Minimal image based on Debian Jessie
- https://www.raspberrypi.org/downloads/raspbian/

```
sudo apt-get update && sudo apt-get upgrade
sudo raspi-config 
```

- Expand SD-card
- Enable SSH
- Enable 1-wire support

Connect DS2423 and try out the 1-wire protocol
- 3V3 (Pin 1) - 4.7 kOhm - DQ
- GIPO4 (Pin 7) - DQ
- GND (Pin 9) - GND

```
sudo modprobe w1-gpio pullup=1
sudo modprobe w1_ds2423
```

The DS2423 device should now be visible under a path similar to /sys/bus/w1/devices/1d-0000000f9d60

```
$ cat /sys/bus/w1/devices/1d-0000000f9d60/w1_slave 
00 00 00 00 00 00 00 00 00 ec e1 00 ff ff 00 00 ff ff 80 08 fd ff 40 00 ff ff 00 00 ff ff 00 00 ff f7 20 00 cf ff 00 00 ff ff crc=YES c=0
02 00 00 00 00 00 00 00 00 db fd 00 ff fd 28 00 ff ff 00 00 ff f7 00 00 ff ff 00 00 ff ef 10 00 ff df 00 02 ff ff 00 00 ff ff crc=YES c=0
00 73 00 00 00 00 00 00 00 fa d0 00 ff fb 00 00 ff fd 00 20 f7 ff 02 01 bf ff 00 00 ff ff 05 00 ff ff 00 00 7f ff 00 00 ff ff crc=YES c=115
01 58 00 00 00 00 00 00 00 3e fd ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff crc=YES c=88
```

The third row represents the A counter and the fourth row the B counter. In this example A=115 and B=88.
