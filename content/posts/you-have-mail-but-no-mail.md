Title: "You Have Mail" But No Mail on Mac
Date: 2026-03-27
Slug: you-have-mail-but-no-mail-on-mac
Category: Tools
Tags: Mac, Terminal, Zsh
Summary: macOS login shell says "You have mail." but `mail` says "No mail." — here's why and how to fix it.

Every time you open a terminal, it greets you with:

```
You have mail.
```

You type `mail`, expecting some exciting cron failure notification, and get:

```
No mail for &lt;username&gt;
```

Cool. Thanks, computer.

## TL;DR

The file `/var/mail/<username>` exists (maybe even empty or corrupted). The login shell sees it and tells you "You have mail." But `mail` can't parse it as a valid mailbox, so it says there's nothing.

## The Case

This happens on macOS when some process writes to `/var/mail/<username>` — usually `cron` or a system daemon. The file gets created, but either the content is malformed, or it's been partially consumed by another process. What's left is a file that exists (so `login` flags it) but contains no parseable mail (so `mail` has nothing to show).

## The Digging

### Step 1: Check if the file exists

```bash
ls -la /var/mail/$(whoami)
```

In my case:

```
-rw-------@ 1 &lt;username&gt;  mail  1 Mar 26 23:13 /var/mail/&lt;username&gt;
```

1 byte. That's it. A single byte of nothing useful.

### Step 2: Try to read it

```bash
cat /var/mail/$(whoami)
```

No output. The file exists but is effectively empty.

### Step 3: Check the mail queue

```bash
mailq
```

```
postqueue: fatal: Queue report unavailable - mail system is down
```

The mail system (Postfix) isn't even running. Which makes sense — nobody actually uses local mail on a Mac.

## Solution

Clear the file:

```bash
> /var/mail/$(whoami)
```

Verify:

```bash
ls -la /var/mail/$(whoami)
-rw-------@ 1 &lt;username&gt;  mail  0 Mar 27 02:18 /var/mail/&lt;username&gt;
```

0 bytes. Restart your terminal — no more "You have mail."

## Why This Keeps Happening

Something on your system periodically writes to `/var/mail/<username>`. If you want to find the culprit next time, run:

```bash
crontab -l
```

Or check system-level crons:

```bash
ls /etc/cron.d/
ls /etc/periodic/
```

Honestly though, on a dev machine you probably don't care. Just clear the file when it shows up again, or add `> /var/mail/$(whoami)` to your `.zshrc` if it really bothers you. Not the cleanest fix, but who cares — it's local mail on macOS. Nobody is using it.
