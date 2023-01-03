# Created By D&Y
from flask import Flask,request
import datetime
import requests
import sys;
import sqlite3 
import bleach
import json

#Declaretion section 
slackactive="False";  #For On Notificatin use "True"  value, by default it's desabled.
slackurl="<enter your slack webhook url>"


app = Flask(__name__)
#Conteroller----------------------------------------------------------------------
def getUse(total,free):
    return int(total)-int(free)

def GetPercentage(total,free):
    user_ip= getUse(total,free)
    precent=int(user_ip)/int(total)*100
    return round(precent,1)

def addNeed(serverip,net_id,clstdt,str):
    lstdt=GetLrow(serverip,net_id,str)
    if lstdt:
        return False
    else:
        return True

def addNeedexp(serverip,net_id,str,staus):
    lstdt=GetLrowExp(serverip,net_id,str,staus)
    if lstdt:
        return False
    else:
        return True

def slackNeed(total,free):
    prs=GetPercentage(total,free)
    print("Percentage: "+str(prs));
    if int(prs) >= 95:
        return True
    else:
        return False

def slackexpired(subnet_id,servername,severity,serverip,utilization,desc,time):
    if slackactive == "True":
        if None != slackurl:
            url = slackurl
            slack_data = {
                "attachments": [
                    {
                        "color": "#f54531",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Lease expired:\n*<google.com|"+subnet_id+" - Leass expired on "+servername+" >*"
                                }
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Severity :*\n"+severity+""
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Event time :*\n"+time
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Server:*\n"+serverip
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Name:*\n"+servername+""
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Subnet:*\n"+subnet_id+""
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Utilization:*\n"+str(utilization)+"%"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Trigger description:*\n"+desc+""
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            try:
                response = requests.post(url, data=json.dumps(slack_data), headers=headers)
                if response.status_code == 200:
                    print("[i] successfully sent the Slack")
                    return True

            except:
                print("[!] failed to send Slack")
                return False
        else:
            print(f"[!] Slack configuration missing")
            return False



def slacknoexpired(subnet_id,servername,severity,serverip,utilization,desc,time,use,free,total):
    if slackactive == "True":
        if None != slackurl:
            url = slackurl
            slack_data = {
                "attachments": [
                    {
                        "color": "#f54531",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Lease expired:\n*<google.com|"+subnet_id+" - Leass expired on "+servername+" >*"
                                }
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Severity :*\n"+severity+""
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Event time :*\n"+time
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Server:*\n"+serverip
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Name:*\n"+servername+""
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Subnet:*\n"+subnet_id+""
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Utilization:*\n"+str(utilization)+"%"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Consumption:*\n Total : "+str(total)+" , Used : "+str(use)+", Free : "+str(free)
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Trigger description:*\n"+desc+""
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            try:
                response = requests.post(url, data=json.dumps(slack_data), headers=headers)
                if response.status_code == 200:
                    print("[i] successfully sent the Slack")
                    return True

            except:
                print("[!] failed to send Slack")
                return False
        else:
            print(f"[!] Slack configuration missing")
            return False
#Conteroller end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Module---------------------------------------------------------------------------
def sanitize(str):
    return bleach.clean(str)

def checkREIp(ip):
    try:
        conn = sqlite3.connect('dhcpleassDB.db') 
        cursor = conn.cursor()
        #print("Opened database successfully"); 
        print("Checking requester ip."); 
        query=f"select * from serverList where serIp='{ip}' AND serStatus='allow' LIMIT 1;"
        result=cursor.execute(query);
        record=result.fetchall();
        if len(record) != 0:
            for row in record:
                print(row);
                if row[1] == ip:
                    cursor.close() 
                    return True 
                else:
                    cursor.close() 
                    return False 
        else:
            #result is null
            cursor.close() 
            return False
    except sqlite3.Error as error:
        print("Filed! :- "+error)
        return False

def AddData(str,servern,serverip,netid,lstdate,total,use,free,status):
    try:
        conn = sqlite3.connect('dhcpleassDB.db') 
        cursor = conn.cursor()
        print("Opened database successfully");
        print("Going TO add data.") 
        query=f"INSERT INTO DhcpLeass(String,ServerName,ServerIP,nework_id,lastupdate,total,use,free,status) VALUES('{str}','{servern}','{serverip}','{netid}','{lstdate}','{total}','{use}','{free}','{status}');"
        print(query);
        cursor.execute(query);
        conn.commit()
        cursor.close() 
        return True 
    except sqlite3.Error as error:
        print("Filed! :- "+error)
        return False

def GetLrow(serverip,net_id,str):
    try:
        conn = sqlite3.connect('dhcpleassDB.db') 
        print("Opened database successfully"); 
        print("Checking Row in ....")
        query=f"select * from DhcpLeass where  ServerIP='{serverip}' and nework_id='{net_id}' ORDER BY dhcpID DESC LIMIT 1;";
        result=conn.execute(query);
        record=result.fetchall();
        if len(record) != 0:
            for row in record:
                print(row)
                if row[4] == net_id and row[1] == str :
                    print(row[4]+" / "+row[1])
                    conn.close() 
                    return True
                else:
                    conn.close() 
                    return False
        else:
            #result is null
            conn.close() 
            return False
    except sqlite3.Error as error:
        print("Filed! :- "+error)
        return False

def GetLrowExp(serverip,net_id,str,status):
    try:
        conn = sqlite3.connect('dhcpleassDB.db') 
        print("Opened database successfully"); 
        print("Checking Row in ....")
        query=f"select * from DhcpLeass where  ServerIP='{serverip}' and nework_id='{net_id}' ORDER BY dhcpID DESC LIMIT 1;";
        result=conn.execute(query);
        record=result.fetchall();
        if len(record) != 0:
            for row in record:
                print(row)
                if row[4] == net_id and row[1] == str and row[9] == status:
                    conn.close() 
                    return True
                else:
                    conn.close() 
                    return False
        else:
            #result is null
            conn.close() 
            return False
    except sqlite3.Error as error:
        print("Filed! :- "+error)
        return False

#Module end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#View routes-----------------------------------------------------------------------------
@app.route("/" , methods=["POST","GET"])
def stop():
    ip_addr = request.remote_addr
    return '<h3>Access Denied :(<h3>'

@app.route("/api" , methods=["POST","GET"])
def api():
    if request.method == 'POST':
        print(request.form)
        ip_addr = request.remote_addr
        if checkREIp(ip_addr):
            if request.form['code']:
                print("Step1")
                if request.form['code'] == "EG37E23F3FjmfjrL2tMJf7Ux2wnTjrYn23":
                    if request.form['status'] != "":
                        if request.form['status'] == "NoExpire":
                            print("Leass not Expire")
                            string= sanitize(request.form['logStr'])
                            last_update= datetime.datetime.strptime(request.form['lastUpdt'], "%b %d %Y %H:%M:%S") 
                            network_id= sanitize(request.form['netID'])
                            total=sanitize(request.form['total'])
                            free=sanitize(request.form['free'])
                            status=sanitize(request.form['status'])
                            ServerName=sanitize(request.form['srname'])
                            use=getUse(total,free);
                            precent=GetPercentage(total,free)
                            if addNeed(ip_addr,network_id,last_update,string):
                                print("Step3")
                                addt=AddData(string,ServerName,ip_addr,network_id,last_update,total,(int(total)-int(free)),free,status)
                                if slackNeed(total,free):
                                    print("Step4")
                                    #sent alert to slackan inset in log file
                                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    slacknoexpired(network_id,ServerName,"Danger",ip_addr,str(precent),"This trigger might indicate Leass expired saturation.",now,use,free,total)
                                    return "Done!!"
                                else:
                                    print("slackNeed false ")
                                    return "Done!!"
                                    #no
                            else:
                                print("No need add")
                                return "No need add!!"

                        elif request.form['status'] == "expired":
                            print("Leass Expired")
                            string= sanitize(request.form['logStr'])
                            network_id= sanitize(request.form['netID'])
                            status=sanitize(request.form['status'])
                            ServerName=sanitize(request.form['srname'])
                            if addNeedexp(ip_addr,network_id,string,status):
                                print("Step3")
                                addt=AddData(string,ServerName,ip_addr,network_id,last_update,total,(int(total)-int(free)),free,status)
                                if slackNeed(total,free):
                                    print("Step4")
                                    #sent alert to slackan inset in log file
                                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    slackexpired(network_id,ServerName,"Danger",ip_addr,str(precent),"This trigger might indicate Leass expired saturation.",now)
                                    return "Done!!"
                                else:
                                    print("slackNeed false ")
                                    return "Done!!"
                                    #no
                            else:
                                print("No need add")
                                return "No need add!!"

                        else:
                            print("Leass Other status")
                            return "Leass Other status!!"
                    else:
                        print("ststus not found")
                        return "ststus not found!!"
                else:
                    print("Code not match.")
                    return "Stop!!!!"
            else:
                return "Stop."
        else:
            return "Access Denied ;)"
    else:
        return "Stop!"

#View end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#main---------------------
if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    app.run(host="0.0.0.0",debug=True,port=8800 ,threaded=True,ssl_context=context)


