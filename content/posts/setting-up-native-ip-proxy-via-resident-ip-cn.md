Title: 通过家庭IP搭建原生IP代理
Date: 2023-05-11 16:04
Slug: setting-up-native-ip-proxy-via-resident-ip-cn
Category: Digital Nomad
Tags: Proxy, Cloudflare, Gost, Certbot, Shadowsocks
Summary: 中文版教程。

许多美国服务，譬如 OpenAI、Netflix 等，都封禁了大批量的机房IP。这也就意味着以前通过租用VPS搭建代理服务器访问这些服务的方法都失效了。

有两种解决方案，这两种方案都仍然需要我们准备一个稳定可靠的 VPS。在这基础上可以选择通过 CloudFlare 的 WARP 客户端来伪装原生IP，或者通过转接一个家庭IP地址来模仿原生IP。

我一开始使用的是 WARP 方案，因为安装维护都很简单。但是由于太多人采用这个方案，巨量的请求都发起自 CloudFlare IP，OpenAI 现在也对这些 IP 采取了渐进的风控手段。

因此我又采用第二种方案，搭建了一个新的代理，目前还没有出现什么问题。以下是部署和使用方法。

## 1. 准备一台VPS

由于我们是要通过VPS连接美国的家庭IP并转发请求，以供客户端连接，所以有两种思路：

1. 选择距离客户端（中国）较近的机房，譬如新加坡、台湾、香港、日本等；
2. 选择距离家庭IP（美国）较近的机房，也就是直接选择美国机房。

实测下来第二种方案更加稳定。你可以自己选择VPS服务商，只要购买美国西部的VPS就可以（比如加州的机房）。VPS 最好选择 Ubuntu 系统。以下的例子也都以 Ubuntu 为准。

## 2. 准备一个家庭IP

Google 关键字 Static Resident IP 即可找到很多服务商。注意，一般会有几种选项，可能会出现比较相近的选项（譬如 static resident IP 和 resident IP），一定要认准关键字，static 和 resident 两个单词必须同时出现才行。

由于我们是从美国的机房直接连接，所以地理位置就无所谓了。

购买到 IP 之后，需要找到对应的代理服务地址和用户名密码。每个服务不太一样，但是你一般可以在代理列表里找到类似 `socks://username:password@IP地址:1234` 的字符串。记录下来，后面要用。

## 3. 准备一个域名

你可以去 CloudFlare 买一个域名。由于只是用来做代理，因此你可以随便找一个便宜的。

> 💡 为什么要用域名？用 IP 地址不行吗？
> 
> 你的 IP 可能会被 GFW 干掉，那就直接完蛋了。但你可以用域名来转接，这样原来的 IP 还可以用。

买好域名之后，在 CloudFlare 中点击你的域名，选择左边菜单的 DNS 设置，添加一条 A 记录，名称随便设置一个好记的字符串，内容填写你的 VPS 的 IP 地址，其它采用默认设置，然后保存。记住这个配置，你后续要使用的域名就是 `你填的字符串.你买的域名`，比如 `foo.bar.com`。

> 💡 为什么要用三级域名？直接用 `[bar.com](http://bar.com)` 不行吗？
> 
> 因为你的域名也可能被 GFW 干掉。被干掉之后，你再配置一个新的 A 记录就复活了。

然后在左边的菜单里选择 SSL/TLS，将加密模式改为完全（严格）。

这样你就完全配置好了。

## 4. 设置服务端

首先通过你的电脑连接到 VPS。以 Mac 为例，打开终端，然后输入 `ssh root@你的VPS地址` 。

登录成功后，首先更新系统：

```bash
apt update
apt upgrade --yes
```

### 4.1 安装 docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```

如果没问题，你会在屏幕上看到一行 `hello world`。

### 4.2 设置防火墙

接下来我们设置防火墙。你需要让你的服务器可以访问 socks 端口的代理，可以接收 http 和 https 端口的请求。

```bash
ufw allow socks # 允许 SOCKS 接口，我们要转发 SOCK 代理。
ufw allow http # 允许 HTTP 访问
ufw allow https # 允许 HTTPS 访问
ufw allow ssh # 如果你的 VPS 使用了其他 SSH 端口，这里要相应修改，譬如 ufw allow 27341
ufw reload # 重新加载防火墙配置
```

这样防火墙就设置好了，你可以通过 `ufw status` 来查看防火墙的状态。 

### 4.3 配置 SSL 证书

接下来，我们给服务器配置 SSL 证书，因为我们需要使用更加安全的 HTTP2 代理。

```bash
snap install --classic certbot # 安装 certbot
certbot certonly --standalone # 用 certbot 配置证书
```

然后根据提示，输入你的邮箱，按 Y 同意使用协议，然后输入你前面购置的域名（对，就是 `[foo.bar.com](http://foo.bar.com)` 那个）。一路确认，不出意外的话你的证书就自动生成并配置好了。

### 4.4 设置代理转发

接下来设置代理转发。首先，在终端里输入：

```bash
nano gost_runner
```

这样会打开一个命令行编辑器。在编辑器中粘贴下面的代码：

```bash
#!/bin/bash

DOMAIN="YOUR.DOMAIN.NAME" # 改为你自己的域名
USER="username" # 设置你自己的代理用户名
PASS="password" # 设置你自己的代理密码
PORT=443
AUTH=$(echo -n ${USER}:${PASS} | base64)
UPSTREAM="YOUR STATIC RESIDENT IP PROXY" # 改为在第二步购买的家庭 IP 地址

BIND_IP=0.0.0.0
CERT_DIR=/etc/letsencrypt
CERT=${CERT_DIR}/live/${DOMAIN}/fullchain.pem
KEY=${CERT_DIR}/live/${DOMAIN}/privkey.pem
sudo docker run -d --name gost \
    -v ${CERT_DIR}:${CERT_DIR}:ro \
    --net=host ginuerzh/gost \
    -L "http2://${BIND_IP}:${PORT}?auth=${AUTH}&cert=${CERT}&key=${KEY}&probe_resist=code:404&knock=www.google.com" \
    -F ${UPSTREAM}
```

> 💡 注意要把 `YOUR.DOMAIN.NAME` 换成你自己的域名， `username` 和 `password` 换成你自己的用户名密码， `UPSTREAM` 就是你在第二步里购买的家庭IP代理。这里设置的用户名密码，就是你后续从客户端连接代理时要用到的。

粘贴并且修改好信息之后，按 `Ctrl + X`，然后再按 `Y` 保存。

然后继续在终端输入：

```bash
chmod +x gost_runner
./gost_runner
```

运行完成之后，你的代理应该就运行起来了。这时候你可以直接在终端里输入以下命令来测试代理是否成功：

```bash
curl -v "https://www.google.com" --proxy "https://DOMAIN" --proxy-user 'USER:PASS'
```

记得把里面的信息换成你自己的。

这样服务端就配置成功了，接下来我们配置客户端。

## 5. 配置客户端

### 5.1 SwitchOmega

最简单的方法就是在 Chrome 中安装 SwitchOmega 插件。网上的教程非常多，你只要填写自己的代理地址（也就是你在 CloudFlare 配置的三级域名），用户名密码（在设置代理转发时填写的 USER 和 PASS）就行。代理类型是 HTTP。

### 5.2 ShadowSocks

使用浏览器插件可以解决 99% 的问题，但有的时候你需要给 app 设置代理。一种选择是直接设置操作系统的全局代理，但是我们希望实现该代理的代理，不需要代理的就不代理，那么可以选择 ShadowSocks 客户端配合 GFW List。

这样我们就需要在客户端也做一次代理转发，把服务端的 HTTP2 代理转发成 ShadowSocks 代理，再使用 ShadowSocks 客户端来连接。

以 Mac 系统为例，首先去 Gost 的仓库下载 gost 软件：

https://github.com/ginuerzh/gost/releases

然后打开 Mac 的终端，输入：

```bash
gost -L ss://aes-128-gcm:passcode@:1984 -F 'https://USER:PASS@DOMAIN:443'
```

然后在 ShadowSocks 客户端配置一个新服务器，地址 `127.0.0.1`，端口 `1984`，认证方式选择 `aes-128-gcm`，密码填 `passcode`。保存，连接，搞定。

> 💡 既然 gost 可以直接配置 ShadowSocks 代理，为什么不直接在服务端搭建 ShadowSocks 然后客户端直接连接呢？
> 
> 因为 HTTP2 协议非常安全，看起来就是普通的网络流量；而 ShadowSocks 是历史悠久的协议，太容易被查。因此我们只是在本机运行，就不会有被查的风险。

</aside>

### 5.3 其他选择

你也可以选择用 Clash 之类的代理软件来管理规则。Clash 的配置规则较为复杂，且并非完全开源（Windows 版本是闭源），有需求可以自行搜索 Clash 配置教程，网上也有很多。

### 5.4 验证代理

还是在 Mac 的终端中输入：

```bash
curl ipinfo.io
```

如果代理成功了，你会看到这样的输出：

```bash
{
  "ip": "YOUR IP",
  "city": "Ashburn",
  "region": "Virginia",
  "country": "US",
  "loc": "39.0437,-77.4875",
  "org": "AS7018 AT&T Services, Inc.",
  "postal": "20147",
  "timezone": "America/New_York",
  "readme": "https://ipinfo.io/missingauth"
}
```

这样你就成为了一个数字美国人，可以放心大胆地使用各种服务了。