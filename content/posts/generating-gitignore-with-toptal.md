Title: Simplify Your Project Setup with Gitignore.io
Category: Coding
Tags: gitignore, command line, project setup, version control, productivity
Summary: I share how to use Gitignore.io to generate a .gitignore file for your project, simplifying your setup process.
Date: 2023-08-14 21:57:24
Slug: generating-gitignore-with-toptal

## The Tool

When starting a new project, there's always a chore to be done: creating the `.gitignore` file.

I've been using [Gitignore.io][0] for a long time. It's a great tool that allows you to generate a `.gitignore` file for your project based on the OS, IDE and programming language you're using.

You can always visit the [website][0] in your browser and manually type the keywords to generate the file. But there's a better way: using the command line.

## CLI

Since the generated file is based on keywords, we can use the `curl` command to generate the file.

```bash
curl -sLw "https://www.toptal.com/developers/gitignore/api/macos,visualstudiocode" >> .gitignore
```

You can also write a function in your `.bashrc` or `.zshrc` file to make it easier to use.

```bash
function gi() {
    curl -sLw "\n" https://www.toptal.com/developers/gitignore/api/$@ ;
}
```

Now you can use the `gi` command to generate the `.gitignore` file.

```bash
gi macos,visualstudiocode
```

## Global Gitignore

But we are lazy, so the less typing the better. You can create a global `.gitignore_global` file in your home directory that will be used for all your projects.

```bash
gi macos,visualstudiocode >> ~/.gitignore_global
```

`git` will automatically use this file. If not, you can add it manually.

```bash
git config --global core.excludesfile ~/.gitignore_global
```

[0]: https://www.toptal.com/developers/gitignore