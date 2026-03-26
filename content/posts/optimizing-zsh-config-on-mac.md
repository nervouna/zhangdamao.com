Title: Optimizing Your Zsh Config on Mac
Date: 2026-03-26
Slug: optimizing-zsh-config-on-mac
Category: Coding
Tags: Zsh, Mac, Terminal, Oh My Zsh
Summary: Clean up your .zshrc, set up history properly, add useful plugins, and manage proxy with a toggle.

If you installed Oh My Zsh and never touched your `.zshrc` again, you're sitting on 100+ lines of commented-out template garbage. Here's how to clean it up and actually make your shell useful.

## Step 1: Clean up .zshrc

Your default `.zshrc` probably looks like this:

```bash
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time Oh My Zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# ... 80 more lines of comments ...

plugins=(git)

source $ZSH/oh-my-zsh.sh

# ... even more comments ...
```

Strip it down to what actually matters:

```bash
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

# Custom configs
for file in ~/Develop/Config/ZSH/*; do
    [ -f "$file" ] && source "$file"
done

export PATH="$HOME/.local/bin:$PATH"
```

I keep my custom configs in a separate directory and source them all in a loop. This way each concern (aliases, proxy, language runtimes) lives in its own file.

## Step 2: Set up shell history

The default history settings are terrible. Your shell forgets everything after 30 commands.

Create a `history.zsh` in your custom config directory:

```bash
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
```

Now your history survives across sessions, deduplicates entries, and shares between multiple terminal windows. Prefix a command with a space if you don't want it recorded.

## Step 3: Install useful plugins

The default Oh My Zsh only gives you `git`. Install these two — they're life changing:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Then add them to your plugins list:

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

- **zsh-autosuggestions** — shows ghost text suggestions from your history as you type. Press right arrow or End to accept.
- **zsh-syntax-highlighting** — highlights commands in green if valid, red if not. You'll catch typos before hitting Enter.

## Step 4: Add some aliases

Create an `aliases.zsh`:

```bash
# Navigation
alias ..='cd ..'
alias ...='cd ../..'

# ls
alias ll='ls -la'
alias la='ls -A'

# Git shortcuts
alias gs='git status'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -20'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Homebrew
alias brewup='brew update && brew upgrade && brew cleanup'
alias brewd='brew doctor'
alias brewls='brew list --versions'
```

The safety aliases make `rm`, `cp`, and `mv` prompt before overwriting. You'll thank yourself the day you almost delete something important.

## Step 5: Toggle proxy on and off

If you use a proxy (and you probably do if you're in China), don't hardcode it in your shell config. That breaks things when you don't need it — like accessing domestic services or local development servers.

Instead, use functions:

```bash
proxy() {
  export https_proxy=http://127.0.0.1:7890
  export http_proxy=http://127.0.0.1:7890
  export all_proxy=socks5://127.0.0.1:7890
  export no_proxy=localhost,127.0.0.1,::1,*.cn
  echo "Proxy enabled"
}

unproxy() {
  unset https_proxy http_proxy all_proxy no_proxy
  echo "Proxy disabled"
}
```

Type `proxy` to turn it on, `unproxy` to turn it off. Simple.

## Step 6: Guard your source commands

If you have config files that reference tools that might not be installed (like Rust), wrap them in a check:

```bash
if [ -d "$HOME/.cargo" ]; then
  export CARGO_HOME="$HOME/.cargo"
  export RUSTUP_HOME="$HOME/.rustup"
  [ -f "$HOME/.cargo/env" ] && source "$HOME/.cargo/env"
fi
```

This prevents annoying `no such file or directory` errors on every shell startup.

## Final result

After all this, your `.zshrc` goes from 113 lines of mostly comments to 13 lines of actual config. Your shell starts faster, remembers more, suggests commands, highlights errors, and your proxy doesn't get in the way.

Open a new terminal and everything just works.
