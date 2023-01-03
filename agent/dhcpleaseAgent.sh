#!/bin/bash
# Created By D&Y
# dhcpleaseAgent
#--------------------------------------
source config.sh
i=0
while :
do
    if [ -f $ConfLoc ]; then
        echo "[`date`] Dhcp config file found" >> /var/lib/dhcpleaseAgent/agent.log
        if [ -s $ConfLoc ]; then
            echo "[`date`] File is not null">> /var/lib/dhcpleaseAgent/agent.log
        else
            echo "[`date`] File is null">> /var/lib/dhcpleaseAgent/agent.log
            break
        fi
    else
        echo "[`date`] Dhcp config file Not found" >> /var/lib/dhcpleaseAgent/agent.log
        break
    fi 
    cat $ConfLoc |grep "subnet [0-9][0-9]"| awk '{print $2","$4}'> sub.csv
    if [ -f sub.csv ]; then
        echo "[`date`] Dhcp list file found" >> /var/lib/dhcpleaseAgent/agent.log
        if [ -s sub.csv ]; then
            echo "[`date`] File is not null">> /var/lib/dhcpleaseAgent/agent.log
        else
            echo "[`date`] File is null">> /var/lib/dhcpleaseAgent/agent.log
            break
        fi
    else
        echo "[`date`] Dhcp list file Not found";>> /var/lib/dhcpleaseAgent/agent.log
        break
    fi
    if [ -f $LogLoc ]; then
        echo "[`date`] Log file found" >> /var/lib/dhcpleaseAgent/agent.log
        if [ -s $LogLoc ]; then
            echo "[`date`] Log file not null">> /var/lib/dhcpleaseAgent/agent.log
        else
            echo "[`date`] Log file Null">> /var/lib/dhcpleaseAgent/agent.log
            break
        fi
    else
        echo "[`date`] Log file not found" >> /var/lib/dhcpleaseAgent/agent.log
        break
    fi

    while IFS=, read -r ip subnet
    do
        logStr=$(cat $LogLoc | grep -e $ip'/[0-9][0-9]'|grep -e "total" -e "free"|tail -n 1);
        if [ -z "$logStr" ];then
            echo "[`date`] No need send, data is null" >> /var/lib/dhcpleaseAgent/agent.log
        else        
            #netID=$(echo $logStr |awk '{print $9}'|tail -n 1);
            netID=$(echo $logStr |grep -P -i -o '([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2])) ' | awk '{print $1}'|tail -n 1); 
            year=`date +"%Y"`
            lastUpdt=$(echo $logStr |awk '{print $1" "$2" '$year' "$3}')
            #total=$(echo $logStr |awk '{print $11}'|tail -n 1);
            total=$(echo $logStr |grep -P -i -o 'to([A-Za-z0-9]+( [A-Za-z0-9]+)+)'|awk '{print $2}'|tail -n 1);
            #free=$(echo $logStr|awk '{print $13}'|tail -n 1);
            free=$(echo $logStr|grep -P -i -o 'to([A-Za-z0-9]+( [A-Za-z0-9]+)+)'|awk '{print $4}'|tail -n 1);
            check_expire_no=$(cat $LogLoc | grep "$(date +'%b %d %H')"|grep "network $ip/[0-9][0-9]: no free leases"|tail -n 1)
            if [ -z $check_expire_no ];then
                    echo "[Status]: leases not expired!" >> /var/lib/dhcpleaseAgent/agent.log
                    status="NoExpire";
            else
                    echo "[Status]: leases expired!" >> /var/lib/dhcpleaseAgent/agent.log
                    status="expired";
            fi
            #echo section -------------------------
            echo "[Server_name]: $ServerName" >> /var/lib/dhcpleaseAgent/agent.log
            echo "[ServerIp]: $IpAdd">> /var/lib/dhcpleaseAgent/agent.log
            echo "[Log String]: $logStr">> /var/lib/dhcpleaseAgent/agent.log
            echo "[Last Update]: $lastUpdt">> /var/lib/dhcpleaseAgent/agent.log
            echo "[IP]: $ip and [Subnet]:$subnet">> /var/lib/dhcpleaseAgent/agent.log
            echo "[Report]: [Netowrk]: $netID,[Total]: $total,[Free]: $free">> /var/lib/dhcpleaseAgent/agent.log
            echo "[Status]: $status">> /var/lib/dhcpleaseAgent/agent.log
            
            if [ $status == "expired" ];then
                sub=$(curl -k -d "code=EG37E23F3FjmfjrL2tMJf7Ux2wnTjrYn23&logStr=$check_expire_no&netID=$netID&status=$status&srname=$ServerName" -X POST $IpAdd)
                echo $sub >> /var/lib/dhcpleaseAgent/agent.log
            elif [ $status == "NoExpire" ];then
                sub=$(curl -k -d "code=EG37E23F3FjmfjrL2tMJf7Ux2wnTjrYn23&logStr=$logStr&lastUpdt=$lastUpdt&netID=$netID&total=$total&free=$free&status=$status&srname=$ServerName" -X POST $IpAdd)
                echo $sub >> /var/lib/dhcpleaseAgent/agent.log
            fi
        fi

    done < sub.csv
    if [ $i -eq 1000 ];then
        rm -rf /var/lib/dhcpleaseAgent/agent.log
        $i=0
    fi
    i=$(($i + 1))
    echo $i
    sleep $duration
done
