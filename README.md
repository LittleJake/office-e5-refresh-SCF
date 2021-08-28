# Office E5 Refresh SCF
修改自github action版AutoApiSecret-加密版。

由于github的TOS，禁止使用action调用相关程序。

因此在 [ZYong9908/AutoApiSecret-1](https://github.com/ZYong9908/AutoApiSecret-1)基础上修改为腾讯云SCF版本。



## Requirement

1. 需要Redis保存refresh_token（可以注册Redislab获取30MB的免费redis服务器）

2. 腾讯云开启云函数功能（拥有免费配额）



## 配置教程

1. 下载代码zip包：[main.zip](https://github.com/LittleJake/office-e5-refresh-SCF/archive/refs/heads/main.zip)

2. 解压`main.zip`，找到`token.txt`，填入refresh_token

3. 获取refresh_token参考：[获取微软Office 365应用APPID、secret、access_token、refresh_token等](https://blog.littlejake.net/archives/481/)

4. 打开云函数页面：https://console.cloud.tencent.com/scf/list-create，新建函数

   ![模板1](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828210618.png)

   打开高级配置：

   ![高级配置](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828210929.png)

   打开触发配置：

   ![模板3](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828211214.png)

## 运行截图

![运行](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210828211457.png)



## 感谢

@ZYong9908



## 开源协议

[Apache2.0](LICENSE)



## PS

[原作者说明](README.old.md)