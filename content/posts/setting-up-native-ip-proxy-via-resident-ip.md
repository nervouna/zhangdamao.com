Title: Setting Up Native IP Proxy via Resident IP
Date: 2023-05-11 16:04
Category: Digital Nomad
Tags: Proxy, Cloudflare, Gost, Certbot, Shadowsocks
Summary: Connecting to location restricted services using a chain of proxies.

点击前往[中文版教程](setting-up-native-ip-proxy-via-resident-ip-cn.html)。

Many American services such as OpenAI and Netflix have banned large numbers of data center IPs, which means that the method of accessing these services by renting a VPS to set up a proxy server has become ineffective.

There are two solutions, both of which still require us to prepare a stable and reliable VPS. On this basis, you can choose to disguise the native IP via CloudFlare's WARP client or simulate the native IP by forwarding to a Resident IP.

I initially used the WARP solution because installation and maintenance were straightforward. However, too many people chose this option, and OpenAI now gradually implements risk control measures against these IPs.

Therefore, I adopted the second solution, set up a new proxy, and nothing has gone wrong so far. Below is the deployment and usage method.

## 1. Prepare a VPS

Since we are connecting to a familial IP in the U.S. through a VPS to forward requests to clients, there are two ways of thinking:

1. Choose a data center closer to the client (China), such as Singapore, Taiwan, Hong Kong, or Japan;
2. Choose a data center close to the Resident IP (US), i.e., directly select a US data center.

Empirical evidence shows that the second solution is more stable. You can choose any VPS service provider, as long as you purchase a VPS in the US West (such as a Californian data center); Ubuntu system is preferable. The examples below are based on Ubuntu.

## 2. Prepare a Resident IP

By entering keywords like "Static Resident IP" into Google, you can find many service providers. Usually, there are several options, and there may be similar options (such as static resident IP and resident IP), but the keywords must have both the "static" and "resident" words.

Since we are directly connecting from a US data center, geographical location is irrelevant.

After purchasing the IP, you need to find the corresponding proxy service address and username and password. Although each service is different, you can usually find something like socks://username:password@IP address:1234 in the proxy list. Write it down because you will need it later.

## 3. Prepare a domain name

You can buy a domain name from CloudFlare. Because it is only used as a proxy, you can choose a cheap one.

> 💡 Why use a domain name? Can't I use an IP address directly?
> 
> Your IP may be blocked by the GFW, then you are done for. But you can use a domain name to redirect, so your original IP can still be used.

After purchasing the domain name, click "DNS setting" on the left menu, add an A record, and set a name for an easy-to-remember string, fill in the IP address of your VPS for content with the other parameters set by default. Then save it. Remember this configuration, your domain name will be the string you entered "your domain name".

> 💡 Why use a third-level domain name? Can't I use "bar.com" directly?
> 
> Because your domain name may also be blocked by the GFW. After being blocked, you can configure a new A record, then you will be resurrected.

Then select SSL/TLS from the left menu, and change the encryption mode to Full(strict).

Now you have fully configured everything.

## 4. Set up the server

First connect to the VPS via your computer. Take Mac as an example, open the terminal, and then enter "ssh root@your VPS address".

After successful login, first update the system:

```bash
apt update
apt upgrade --yes
```

### 4.1 Install Docker

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

If there is no problem, you will see "hello world" on the screen.

### 4.2 Set up firewall

Next, we need to set up a firewall. You need to allow your server to access the SOCKS proxy port and receive requests on the HTTP and HTTPS ports.

```bash
ufw allow socks # Allow the SOCKS interface, as we want to forward the SOCKS proxy. 
ufw allow http # Allow HTTP access
ufw allow https # Allow HTTPS access
ufw allow ssh # If your VPS uses a different SSH port, make sure to modify this; for example, ufw allow 27341
ufw reload # Reload the firewall configuration
```

With that, your firewall is set up. You can check the firewall status using `ufw status`.

### 4.3 Configure SSL certificate

Next, we will configure an SSL certificate for our server, as we need to use a more secure HTTP2 proxy.

```bash
snap install --classic certbot # Install certbot
certbot certonly --standalone # Use certbot to configure a certificate
```

Then, follow the prompts to enter your email, agree to the terms of service by typing Y, and enter the domain you previously purchased (yes, the `foo.bar.com` one). Confirm everything, and assuming nothing goes wrong, your certificate will be automatically generated and configured.

### 4.4 Set up proxy forwarding

Next, we will set up proxy forwarding. First, enter the following in the terminal:

```bash
nano gost_runner
```

This will open up a command line editor. Paste the following code into the editor:

```bash
#!/bin/bash

DOMAIN="YOUR.DOMAIN.NAME" # Change to your own domain name.
USER="username" # Set your own proxy username
PASS="password" # Set your own proxy password
PORT=443
AUTH=$(echo -n ${USER}:${PASS} | base64)
UPSTREAM="YOUR STATIC RESIDENT IP PROXY" # Change this to the Resident IP address proxy you purchased in step 2

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

> 💡 Note that you should replace `YOUR.DOMAIN.NAME` with your own domain name, `username` and `password` with your own credentials, and `UPSTREAM` should be the Resident IP proxy you purchased in Step 2. The username and password you set here will be used when connecting to the proxy from the client later on.

Once you've pasted and modified the above information, press `Ctrl + X`, then press `Y` to save.

Then, enter the following into the terminal:

```bash
chmod +x gost_runner
./gost_runner
```

Once it's been set up, your proxy should be running. You can test whether the proxy was set up successfully in the terminal by entering the following:

```bash
curl -v "https://www.google.com" --proxy "https://DOMAIN" --proxy-user 'USER:PASS'
```

Remember to replace the inputs with your own information.

That's it for the server setup. Next, we'll configure the client.

## 5. Configure the client

### 5.1 SwitchOmega

The easiest way to configure the client is to install the SwitchOmega Chrome plugin. There are many tutorials online - all you need to do is fill in your proxy address (the third-level domain name you configured in CloudFlare), your username and password (the ones you entered when setting up proxy forwarding), and select the HTTP proxy type.

### 5.2 ShadowSocks

Using a browser plugin can solve 99% of your problems, but sometimes you need to set up a proxy for your apps. One option is to set up a global proxy for your operating system, but we want to implement a proxy for the proxy, so that we only need to proxy what needs to be proxied. In that case, you can choose ShadowSocks client with GFW List.

Using Mac as an example, first go to the Gost repository to download the gost software:

https://github.com/ginuerzh/gost/releases

Then, open the Mac terminal and type:

```bash
gost -L ss://aes-128-gcm:passcode@:1984 -F 'https://USER:PASS@DOMAIN:443'
```

Then, configure a new server in the ShadowSocks client with the address `127.0.0.1`, port `1984`, select authentication method `aes-128-gcm`, and enter `passcode` as the password. Save and connect - you're all set.

>💡 Since gost can be configured directly with ShadowSocks proxies, why don't we set up ShadowSocks on the server and connect directly with the client?
> 
> Because the HTTP2 protocol is very secure and looks like ordinary network traffic; ShadowSocks is an older protocol that is much easier to detect. Therefore, we only run it locally to avoid the risk of being detected.

### 5.3 Other alternatives

You can also choose to manage rules using proxy software such as Clash. The Clash configuration rules are more complex and not completely open source (the Windows version is closed source), but there are many tutorials available online if you're interested.

### 5.4 Verify the proxy

On your Mac terminal, type:

```bash
curl ipinfo.io
```

If the proxy was successful, you should get output like this:

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

Now you've become a digital American and can confidently use various online services.