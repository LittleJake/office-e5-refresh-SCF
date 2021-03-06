# Office E5 Refresh SCF
修改自github action版AutoApiSecret-加密版。

由于github的TOS，禁止使用action调用相关程序。

因此在 [ZYong9908/AutoApiSecret-1](https://github.com/ZYong9908/AutoApiSecret-1)基础上修改为腾讯云SCF版本。



## Requirement

### 云函数

- 需要Redis保存refresh_token（可以注册Redislab获取30MB的免费redis服务器）

- 腾讯云开启云函数功能（拥有免费配额）

### Linux

- 支持`cURL`


## 脚本配置

### 云函数

#### 配置教程

1. 下载代码zip包：[main.zip](https://github.com/LittleJake/office-e5-refresh-SCF/archive/refs/heads/main.zip)

2. 解压`main.zip`，找到`token.txt`，填入refresh_token

3. 获取refresh_token参考：[获取微软Office 365应用APPID、secret、access_token、refresh_token等](https://blog.littlejake.net/archives/481/)，视频教程：[AutoApi教程](https://www.bilibili.com/video/av95688306/)，打开权限：

   ```
   #先注册azure应用,确保应用有以下权限:
   #files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
   #user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
   #mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
   #注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用
   ```

4. 打开云函数页面：[https://console.cloud.tencent.com/scf/list-create](https://console.cloud.tencent.com/scf/list-create) ，新建函数。
   > **为了提高访问稳定性，地域选择中国香港**

   ![模板1](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828210618.png)

   打开高级配置：

   ![高级配置](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828210929.png)

   打开触发配置：

   ![模板3](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828211214.png)

#### RedisLab相关参数

* RedisLab服务器信息（域名和端口）
 ![RedisLab](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/202111300019368.png)
* RedisLab服务器信息（连接密码）
 ![RedisLab](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/202111300021201.png)



#### 云函数运行截图

![运行](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828211457.png)


### Linux主机

#### 使用shell脚本运行

> 可以加入到crontab定时执行。

```bash
   git clone https://github.com/LittleJake/office-e5-refresh-SCF/
   cd office-e5-refresh-SCF
   bash e5_refresh.sh
```

![shell配置](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/202205262243679.png)

##### shell脚本运行截图

![运行](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210928221336.png)

#### 使用青龙面板

> 拉取后会自动定时执行：每日 12:15

```bash
docker exec -it qinglong ql raw https://raw.fastgit.org/LittleJake/office-e5-refresh-SCF/main/e5_refresh.sh
```

##### 配置

登录到青龙面板 - 脚本管理，找到对应脚本编辑，填入信息后保存。

![青龙配置](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/202205262248082.png)

![配置随机延迟](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/202205262300305.png)

##### 青龙脚本运行截图

![运行](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/202205262252116.png)

## 感谢

@ZYong9908


## 开源协议

[Apache2.0](LICENSE)


## PS

[原作者说明](README.old.md)
