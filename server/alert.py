# Created By D&Y
# This DhcpAlertScript
#-------------------------------------
import datetime
import requests
import sqlite3 
import json
import sys
import random
import time

#Declaretion section 
slackactive="False";  #For On Notificatin use "True"  value, by default it's desabled.
slackurl="<enter your slack webhook url>"

def maingetdata():
    try:
        conn = sqlite3.connect('dhcpleassDB.db') 
        cursor = conn.cursor()
        print("Opened database successfully"); 
        query=f"select serIp from serverList"
        result=cursor.execute(query);
        record=result.fetchall();
        if len(record) != 0:
            mass1="";
            for row in record:
                #('10.32.80.6',)
                #print(row);
                getdata(row[0])
                
        else:
            #result is null
            cursor.close() 
    except sqlite3.Error as error:
        print("Filed! :- "+error)

    return 0


def getdata(primary):
    mass=[False,""]
    try:
        conn = sqlite3.connect('dhcpleassDB.db') 
        cursor = conn.cursor()
        print("Opened database successfully"); 
        query=f"select nework_id,( select ServerName from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as ServerName, ( select ServerIP from DhcpLeass t2 where  t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as ServerIP, ( select lastupdate from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as lastupdate, ( select total from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as total, ( select use from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as use, ( select free from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as free, ( select status from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as status, ( select datetime(dhcpADD, 'localtime') from DhcpLeass t2 where t2.ServerIP='{primary}' AND t.nework_id = t2.nework_id ORDER BY dhcpID DESC LIMIT 1 ) as dhcpADD from DhcpLeass t where ServerIP='{primary}' GROUP BY nework_id;"
        result=cursor.execute(query);
        record=result.fetchall();
        if len(record) != 0:
            mass1="";
            loc=""
            lst=""
            count=0
            for row in record:
                mass[0]=True
                #('172.16.0.0/22', 'IBC DHCP Primary Server', '172.16.8.8', '2022-12-29 10:13:05', '1011', '516', '495', 'NoExpire', '2022-12-29 15:47:58')
                #print(row);
                precent=round((int(row[5])/int(row[4])*100) ,1)
                mass1=mass1+f"*{row[0]} ({str(precent)}%) ({row[2]})* --> *Total* : {row[4]}  *Free* : {row[6]}  *Use* : {row[5]}\n"
                loc=row[1];
                lst=row[3]
                count=count+1
                if count == 25:
                    dy=f"*LastUpdate* : {lst}\n\n"+str(mass1)
                    slackexpired(dy ,loc);
                    count=0
                    mass1="";

                

            mass[1]=f"*LastUpdate* : {lst}\n\n"+str(mass1); 
            print(mass[1]) 
            if mass[0] == True:
                slackexpired(mass[1] ,loc);
        else:
            #result is null
            cursor.close() 
    except sqlite3.Error as error:
        print("Filed! :- "+error)

    return 0



def slackexpired(data1,loc):
    color=["#8E44AD","#2E86C1","#2980B9","#2E86C1","#17A589","#229954","#F1C40F","#D0D3D4","#2E4053","#DFFF00","#40E0D0","#CCCCFF","#6495ED","#FFBF00","#FF7F50"]
    val=random.randint(0, 14)
    co=color[val];
    if slackactive == "True":
        if None != slackurl:
            url = slackurl
            now = datetime.datetime.now()
            dt_string = now.strftime("%d %b,%Y %I:%M %p")
            hed=f"[ {dt_string} ] {loc} report:"
            slack_data = {
    "attachments": [
        {
            "color": ""+co+"",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": hed
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": data1
                    }
                }
            ]
        }
    ]    
}
            #print(slack_data);
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            try:
                response = requests.post(url, data=json.dumps(slack_data), headers=headers)
                if response.status_code == 200:
                    print("[i] successfully sent the Slack")
                    return True
                else:
                     print(f"[!] {response.status_code}")

            except:
                print("[!] failed to send Slack")
                return False
        else:
            print(f"[!] Slack configuration missing")
            return False

maingetdata()
time.sleep(14400)
# getdt=getdata()
# if getdt[0]:
#     #print(getdt[1])
#     asaa=str(getdt[1])
#     print(type(asaa))
#     #slackexpired(asaa);
