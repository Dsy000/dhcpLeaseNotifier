#!/bin/bash
# Created By D&Y
# dhcpleaseAgent configuration file.
# serverName
ServerName="Primary DHCP Server/Secondary DHCP Server"

# ServerIP/url with porn ip:port/location
IpAdd="https://<server_ip>:8800/api"

# SSL Certificate.
SSLkeyFileLoc=""

# log file location.
LogLoc="/var/log/messages";
# vim /var/log/messages      in  CentOS7
# vim /var/log/syslog        in  Ubuntu 21.10

# configuration file location.
ConfLoc="/etc/dhcp/dhcpd.conf";

# Duration in second
duration=600
# 10 min 600 sec

