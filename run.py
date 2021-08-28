# -*- coding: UTF-8 -*-
#先注册azure应用,确保应用有以下权限:
#files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
#user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
#mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
#注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用
import requests as req
import redis
import json,sys,time,os,random

num = 0
path = os.getcwd() + r'/token.txt'
REDIS_HOST = os.environ.get('redis_host')
REDIS_PORT = int(os.environ.get('redis_port'))
REDIS_PASSWORD = os.environ.get('redis_password')

def update_token(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'}
    data= {'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':os.environ.get('client_id'),
          'client_secret':os.environ.get('client_secret'),
          'redirect_uri':'http://localhost:53682/'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data,headers=headers)
    jsontxt = json.loads(html.text)
    access_token = jsontxt['access_token']
    refresh_token = jsontxt['refresh_token']
    return access_token, refresh_token

def load_token():
    with open(path, "r") as fo:
        refresh_token = fo.read()

    try:
        with redis.Redis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD) as red:
            if red.exists(os.environ.get('client_id')):
                refresh_token = red.get(os.environ.get('client_id'))
            else:
                red.set(os.environ.get('client_id'), refresh_token)
            
            access_token, refresh_token = update_token(refresh_token)
            red.set(os.environ.get('client_id'), refresh_token)
            return access_token
    except Exception as e:
        print(e)
        print("连接Redis出错，尝试使用原refresh_token")
        access_token, refresh_token = update_token(refresh_token)
        return access_token

def add_count(type=""):
    global num
    num+=1
    print(type + "调用成功"+str(num)+'次')
    time.sleep(random.randint(0,10))

def main():
    print("任务开始")
    time.sleep(random.randint(0,30))
    access_token = load_token()
    localtime = time.asctime(time.localtime(time.time()))
    headers={'Authorization':access_token,'Content-Type':'application/json'}
    try:
        if req.get(r'https://graph.microsoft.com/v1.0/me/drive/root',headers=headers).status_code == 200:
            add_count("drive/root")
        if req.get(r'https://graph.microsoft.com/v1.0/me/drive',headers=headers).status_code == 200:
            add_count("me/drive")
        if req.get(r'https://graph.microsoft.com/v1.0/drive/root',headers=headers).status_code == 200:
            add_count("drive/root")
        if req.get(r'https://graph.microsoft.com/v1.0/users ',headers=headers).status_code == 200:
            add_count("users")
        if req.get(r'https://graph.microsoft.com/v1.0/me/messages',headers=headers).status_code == 200:
            add_count("me/messages") 
        if req.get(r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',headers=headers).status_code == 200:
            add_count("me/mailFolders/inbox/messageRules")  
        if req.get(r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',headers=headers).status_code == 200:
            add_count("me/mailFolders/Inbox/messages/delta")
        if req.get(r'https://graph.microsoft.com/v1.0/me/drive/root/children',headers=headers).status_code == 200:
            add_count("me/drive/root/children")
        if req.get(r'https://api.powerbi.com/v1.0/myorg/apps',headers=headers).status_code == 200:
            add_count("myorg/apps")
        if req.get(r'https://graph.microsoft.com/v1.0/me/mailFolders',headers=headers).status_code == 200:
            add_count("me/mailFolders")
        if req.get(r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',headers=headers).status_code == 200:
            add_count("me/outlook/masterCategories")
        
        print('此次运行结束时间为 :', localtime)
    except:
        print("pass")
        pass
        
def main_handler(event, context):
    for _ in range(3):
        main()

