Title: SSH Authentication Fails on github.com While Works on Other Servers
Date: 2023-07-08 01:11:00
Slug: github-push-error-via-ssh
Category: Tools
Tags: Git, SSH, GitHub
Summary: DNS pollution leads to authentication failure on github.com

# TL;DR

It's because my DNS was polluted. Github.com was pointed to 127.0.0.1.

I guess that's one of the many benefits for living in China.

Anyway, I changed my DNS server from default to 1.1.1.1 and everything got back to normal.

# The Case

What I was doing:

- Trying to push commits to one of my repos hosted on GitHub
- Authenticating with my public key
- Using SSH protocol (git@github.com:foo/bar.git)

What I got:

- Prompts to provide password for git@github.com, which was not supposed to happen

What I tried when authentication failed:

- Tried `ssh -T git@github.com`, got same result.

What I checked:

- Confirmed my remote url does begin with `git@github.com`
- Confirmed I do have a valid key pair `~/.ssh/id_rsa`
- Confirmed my public key has the same sha256 signature as the key I set up in my GitHub account
- Confirmed my key is being used (`ssh-add -l -E sha256` shows correct result)

# The Digging

#### Checking SSH config

```bash
cat .ssh/config

Host github.com
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_rsa
```

#### Check SSH Agent

```bash
ssh-add -l
3072 SHA256:<SHA256 hash> foo@bar (RSA)
```

#### Check SSH Connection

I checked the result for ssh -vT git@github.com.

<details>
  <summary>Click to see the results</summary>

```bash
ssh -vT git@github.com
OpenSSH_9.0p1, LibreSSL 3.3.6
debug1: Reading configuration data /Users/damao/.ssh/config
debug1: /Users/damao/.ssh/config line 22: Applying options for github
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug1: Connecting to github.com port 22.
debug1: Connection established.
debug1: identity file /Users/damao/.ssh/id_rsa type 0
debug1: identity file /Users/damao/.ssh/id_rsa-cert type -1
debug1: Local version string SSH-2.0-OpenSSH_9.0
debug1: Remote protocol version 2.0, remote software version OpenSSH_9.0
debug1: compat_banner: match: OpenSSH_9.0 pat OpenSSH* compat 0x04000000
debug1: Authenticating to github.com:22 as 'git'
debug1: load_hostkeys: fopen /Users/damao/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: algorithm: sntrup761x25519-sha512@openssh.com
debug1: kex: host key algorithm: ssh-ed25519
debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-ed25519 SHA256:6WZWDsTPiC48vtLxGY9RMIdVhHRf/fLvgjbetnTapsY
debug1: load_hostkeys: fopen /Users/damao/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
debug1: Host 'github.com' is known and matches the ED25519 host key.
debug1: Found key in /Users/damao/.ssh/known_hosts:1
debug1: rekey out after 134217728 blocks
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: rekey in after 134217728 blocks
debug1: get_agent_identities: bound agent to hostkey
debug1: get_agent_identities: ssh_fetch_identitylist: agent contains no identities
debug1: Will attempt key: <KEY> explicit
debug1: SSH2_MSG_EXT_INFO received
debug1: kex_input_ext_info: server-sig-algs=<ssh-ed25519,ssh-rsa,rsa-sha2-256,rsa-sha2-512,ssh-dss,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521>
debug1: kex_input_ext_info: publickey-hostbound@openssh.com=<0>
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,password,keyboard-interactive
debug1: Next authentication method: publickey
debug1: Offering public key: <KEY> explicit
debug1: Authentications that can continue: publickey,password,keyboard-interactive
debug1: Next authentication method: keyboard-interactive
(git@github.com) Password:
```

</details>

#### Check SSH Connection with Other Servers

I can still SSH onto other servers. It's really confusing.

#### Check SSH over HTTPS port

Using SSH over HTTPS port works.

```bash
ssh -T -p 443 git@ssh.github.com
Hi nervouna! You've successfully authenticated, but GitHub does not provide shell access.
```

#### Desperate Attempt

```bash
rm .ssh/known_hosts
ssh -T git@github.com
```

And guess what I got.

```
The authenticity of host 'github.com (127.0.0.1)' can't be established.
ED25519 key fingerprint is SHA256:nnItlekUHPmj3VxIM+UODrHMaIWihzPLBgP/oP0lowE.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

What the FUCK?

# Solution

Change my DNS server from default to 1.1.1.1 and problem solved.

Fuck you and your GFW, sincerely.