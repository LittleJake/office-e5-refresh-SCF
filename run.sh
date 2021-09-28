#!/bin/bash
# 先注册azure应用,确保应用有以下权限:
# files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# 注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用
# 请填写好下面配置CLIENT_ID、CLIENT_SECRET、REFRESH_TOKEN
# 配置开始

CLIENT_ID='CLIENT_ID'
CLIENT_SECRET='CLIENT_SECRET'
REFRESH_TOKEN='REFRESH_TOKEN'

# 配置结束

URLS='https://graph.microsoft.com/v1.0/me/drive/root 
https://graph.microsoft.com/v1.0/me/drive 
https://graph.microsoft.com/v1.0/me/drives 
https://graph.microsoft.com/v1.0/drive/root 
https://graph.microsoft.com/v1.0/users 
https://graph.microsoft.com/v1.0/me/messages 
https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules 
https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta 
https://graph.microsoft.com/v1.0/me/drive/root/children 
https://graph.microsoft.com/v1.0/me/mailFolders 
https://graph.microsoft.com/v1.0/sites/root 
https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
SCRIPT_PATH="$0"

function get_token(){
    resp=`curl -s -X POST \
        --data-urlencode grant_type=refresh_token \
        --data-urlencode refresh_token=$REFRESH_TOKEN \
        --data-urlencode client_id=$CLIENT_ID \
        --data-urlencode client_secret=$CLIENT_SECRET \
        --data-urlencode redirect_uri=http://localhost:53682/ \
        https://login.microsoftonline.com/common/oauth2/v2.0/token`
    
    error=${resp#*error\":\"}
    error=${error%%\"*}
    if [[ $resp =~ '"error"' ]]
    then
        echo "获取access_token失败，错误信息：$error"
        exit 1
    fi

    refresh_token=${resp#*refresh_token\":\"}
    refresh_token=${refresh_token%%\"*}
    access_token=${resp#*access_token\":\"}
    access_token=${access_token%%\"*}
    sed -i "s/^REFRESH_TOKEN.*/REFRESH_TOKEN='${refresh_token}'/g" $SCRIPT_PATH
}

function print_log(){
    echo "["`date`"] $1"
}

print_log "任务开始"
t=`date +%s`
get_token

for url in $URLS
do
    print_log "任务$url"
    result=`curl --connect-timeout 5 -m 5 -s -H "Content-Type: application/json" \
        -H "Authorization: ${access_token}" $url`

    if [[ $result =~ '"error"' ]]
    then
        error=${result#*error\":\"}
        error=${error%%\"*}
        print_log "调用API失败，错误信息：$error"
    else
        print_log "调用成功"
    fi
    sleep 5
done
print_log "任务结束，用时"$((`date +%s`-t))"秒"