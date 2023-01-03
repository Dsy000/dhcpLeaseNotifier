#!/bin/bash
#Created By D&Y
# dhcpleaseAgent installation file
#--------------------------------------
if [ `whoami` != 'root' ];then
    echo "Please run this script as root user"
    exit 1
fi
#Enter your code
echo "OK you are root :)"
echo "Now i am running your script."
mkdir /var/lib/dhcpleaseAgent
if [ -d "/path/to/dir" ] && [ ! -L "/path/to/dir" ];then 
    cp dhcpLeassAgent.service /etc/systemd/system/dhcpLeassAgent.service
    cp dhcpleaseAgent.sh /var/lib/dhcpleaseAgent/dhcpleaseAgent.sh
    cp config.sh /var/lib/dhcpleaseAgent/config.sh
    if [ -f /etc/systemd/system/dhcpLeassAgent.service];then
        systemctl start dhcpLeassAgent.service
        systemctl status dhcpLeassAgent.service
        systemctl enable dhcpLeassAgent.service
    else
        echo "Service file not set."
    fi
else
    echo "Failed to create Directory."
fi
