Title: Quick Setup for Certbot
Date: 2022-09-06 22:00:00
Category: Server
Tags: Certbot
Slug: setup-https-via-certbot
Summary: Certbot, good bot.

It's been a while since I built a website, but now it's so much easier. The following configuration is based on Ubuntu 22.04.1 LTS + nginx 1.18.0.

```bash
sudo snap install core && sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx
sudo certbot renew --dry-run #测试证书续期
```

At this point, accessing your website should already be using the https protocol. To automatically renew, you can create a scheduled task through `crontab -e`:

```bash
0 0 1 * * /usr/bin/certbot renew --force-renewal
```

That's it.