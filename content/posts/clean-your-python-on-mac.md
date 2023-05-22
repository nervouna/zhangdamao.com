Title: Cleaning Up Pythons on Your Mac
Date: 2023-05-23
Slug: clean-pythons-on-mac
Category: Coding
Tags: Python, Mac
Summary: Install Python the right way.

To do a clean Python install (and hopefuly remain that way), here's a brief guide.

## Step 1: Remove all pip packages

```bash
pip uninstall -y -r <(pip freeze)
```

And also remove all pip caches:

```bash
rm -rf ~/Library/Caches/pip/*
```

Finally, remove pip:

```bash
pip uninstall pip
```

## Step 2: Remove all Pythons

```bash
rm -rf ~/Library/Python
brew uninstall python
```

You might run into some error messages when you `brew uninstall python`, indicating that some packages relies on python so that python cannot to be uninstalled. In that case, delete them also.

## Step 3: Clean up path

```bash
vim ~/.zshrc # or whatever shrc you are using.
```

Delete all python related path exports. And don't forget any anaconda / conda shit.

```bash
rm -rf ~/.anaconda*
rm -rf ~/anaconda*
```

## Step 4: Install the one and only Python

```bash
brew install python
```

There you go, you now have a clean global python.