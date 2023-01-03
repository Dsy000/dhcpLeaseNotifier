#!/bin/bash
#Created By D&Y
#--------------------------------------
if [ `whoami` != 'root' ];then
    echo "Please run this script as root user"
    exit 1
fi
#Enter your code
echo "OK you are root :)"
echo "Now i am running your script."
mkdir /var/www/dhcp_api
if [ -d "/path/to/dir" ] && [ ! -L "/path/to/dir" ];then 
    cp dhcpLeassServerAlert.service /etc/systemd/system/dhcpLeassServer.service
    cp dhcpLeassServerAlert.service /etc/systemd/system/dhcpLeassServerAlert.service
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 7300
    cp app.py /etc/systemd/system/app.py
    cp alery.py /etc/systemd/system/alery.py
    if [ -f /etc/systemd/system/dhcpLeassServerAlert.service];then
        systemctl start dhcpLeassAgent.service
        systemctl status dhcpLeassAgent.service
        systemctl enable dhcpLeassAgent.service
        systemctl start dhcpLeassServerAlert.service
        systemctl status dhcpLeassServerAlert.service
        systemctl enable dhcpLeassServerAlert.service
    else
        echo "Service file not set."
    fi
else
    echo "Failed to create Directory."
fi
