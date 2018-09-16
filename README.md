# Setup

Run the following commands:

```
pip install apschedule
sudo nano /boot/config.txt
```
add the following line to the end of the file:
`dtoverlay=w1-gpio`

Then run:
```
sudp raspi-config
```

select `Interfacing Options -> 1-Wire -> enable`
Reboot
