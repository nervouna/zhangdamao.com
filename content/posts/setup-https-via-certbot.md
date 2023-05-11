Title: 快速配置 Certbot
Date: 2022-09-06 22:00:00
Category: 编程
Tags: Certbot
Slug: setup-https-via-certbot

很久没有建站，没想到现在这么方便。以下配置是基于 Ubuntu 22.04.1 LTS + nginx 1.18.0。

```bash
sudo snap install core && sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx
sudo certbot renew --dry-run #测试证书续期
```
这时候访问你的网站，应当已经是 `https` 协议了。要自动续期，可以通过 `crontab -e` 创建定时任务：

```bash
0 0 1 * * /usr/bin/certbot renew --force-renewal
```
这就完事了。