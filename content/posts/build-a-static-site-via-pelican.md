Title: Build a static site via Pelican
Date: 2022-09-06 21:30:14
Slug: build-a-static-site-via-pelican
Category: Coding
Tags: Python, Pelican
Summary: Setting up a static website, without having to install 1,000+ npm packages.

It’s been a while since I wrote a blog, and WordPress just didn't feel right. So, in the end, I decided to build a static website using Pelican.

Requirements
----

You will need the following:

*   A running VPS that you can SSH into
*   A local Python environment, including venv
*   A markdown editor, like Notepad

Setup
----

First, create a working directory and set up a Python virtual environment:

```bash
➜ mkdir -p blog/
➜ cd blog/
➜ python3 -m venv env
➜ source env/bin/activate
```

Then, install Pelican in the virtual environment, along with the markdown option:

```bash
➜ pip install "pelican[markdown]"
```

Next, use `pelican-quickstart` and follow the interactive command prompts; it's usually best to choose the default options. See [Pelican's official documentation](https://docs.getpelican.com/en/latest/quickstart.html) for further details.

Start Writing
----

It is strongly recommended to manage your working directory with `git` before you start writing:

```bash
➜ git init && git add . && git commit -m "(init) blog scaffold"
```

Your working directory should look like this after running `pelican-quickstart`:

```bash
➜ tree -I env . 
├── Makefile 
├── content 
├── output 
├── pelicanconf.py 
├── publishconf.py 
└── tasks.py
```

The `content` directory is where you store all of your markdown files, and the `output` directory is where Pelican stores the generated website files.

Content Formatting
----

In short, you must specify the title and publishing date of your article in the first two lines of the markdown file:

```
Title: Your Title Here.
Date: 2022-09-06 21:30:14
```

A lazy trick is to add an alias in your `bashrc` or `zshrc` to copy the current date to your clipboard with a single command:

```bash
 ➜ alias dt=`date “+%Y-%m-%d %H:%M:%S” | pbcopy` 
```

You can also set up a keyboard shortcut to execute a shell script on a Mac.

Changing Themes
----

The Pelican default theme is downright uncomfortable. You can search for Pelican themes on Google, or go straight to [Pelican Themes](http://www.pelicanthemes.com/) to find one you like.

Installing a theme is straightforward. Themes are generally hosted on GitHub, so you can install them using Git Submodule:

```bash
➜ git submodule add git@github.com:gilsondev/pelican-clean-blog.git
```

The example above uses the [Pelican Clean Blog](https://github.com/gilsondev/pelican-clean-blog) theme that I'm currently using.

Pelican themes use [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) to build. You can define all of the styles yourself. I'm lazy, so I just used the original theme.

Deployment
----

Because Pelican generates static files, all you need to do is copy the output directory contents to your server to deploy it. I used `rsync`. Create a script:

```bash
➜ cat > deploy
#!/bin/sh
pelican
export blog_output="/path/to/your/blog/output"
export prod_dir="/serving/dir/on/your/server/"
rsync -rvz $blog_output/* user@host:$prod_dir
```

Then `chmod +x deploy`. When you're ready to deploy, run `./deploy`. You could also put it into the post-commit hook of your Git repository. The `-v` flag is purely to make the process less boring.

After deployment, you can see the final result. For more detailed explanations, see the following links:

1.  [docs.getpelican.com](https://docs.getpelican.com/en/latest/index.html)
2.  [git-scm.com](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
3.  [linux.die.net/man/1/rsync](https://linux.die.net/man/1/rsync)