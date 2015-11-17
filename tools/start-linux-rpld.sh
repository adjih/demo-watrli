#! /bin/sh
#---------------------------------------------------------------------------

echo "Starting border router"

sudo killall rpld
sudo modprobe ipv6
#sudo ip -6 address add 2015:3:18:1111::1/64 dev usb0
sudo ip -6 address add 2001:db8:1::1/64 dev usb0
sudo ifconfig usb0 up
sudo ./rpld-adjih/rpld -i usb0 -d 2001:db8:1::1 -v

#---------------------------------------------------------------------------
