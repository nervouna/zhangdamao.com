Title: 通过 Pelican 快速部署静态网站
Date: 2022-09-06 21:30:14
Category: 编程
Tags: Python, Pelican
Slug: build-a-static-site-via-pelican

很久没有写博客，想要重新捡起来，搭了一个 WordPress 各种不顺手，最后决定用 Pelican 搭建一个静态网站。

准备工作
----

你需要准备以下条件：

*   一个正常工作的，可以通过 SSH 登录的 VPS；
*   本地 Python 环境，包括 venv；
*   一个 markdown 编辑器，记事本也可以。

搭建环境
----

首先搭建工作目录，创建并激活 Python 虚拟环境：

```bash
➜ mkdir -p blog/
➜ cd blog/
➜ python3 -m venv env
➜ source env/bin/activate
```

在虚拟环境安装 Pelican，注意需要加上 markdown 选项。

```bash
➜ pip install "pelican[markdown]"
```

然后 `pelican-quickstart`，跟着交互式命令一路走下来，大部分情况选择默认选项就行。详细可以参考 Pelican 的[官方文档](https://docs.getpelican.com/en/latest/quickstart.html)。

开始写作
----

在开始写作之前，强烈建议把工作目录通过 `git` 管理起来。

```bash
➜ git init && git add . && git commit -m "(init) blog scaffold"
```

Git 的提交记录也可以作为自己创作的历史记录。

完成 `pelican-quickstart` 后，你的工作目录结构应该如下：

```bash
➜ tree -I env . 
├── Makefile 
├── content 
├── output 
├── pelicanconf.py 
├── publishconf.py 
└── tasks.py
```

其中 `content` 目录是存放所有 markdown 文件的地方，output 是 pelican 默认的输出文件夹，生成的静态网站文件就会出现在这里。

接下来要做的事情就很简单了。用 markdown 来写自己的内容，存放到 `content` 目录，然后用 `pelican` 生成静态页即可。

内容格式
----

简单来说，你需要在 markdown 文件的前两行显式地说明这篇文章的标题和创作日期。

```
Title: Your Title Here.
Date: 2022-09-06 21:30:14
```

一个偷懒小技巧：在你的 `bashrc` 或者`zshrc` 中加一个 alias，以后输入 Date 的时候就不用很愚蠢地手敲了。

```bash
 ➜ alias dt=`date “+%Y-%m-%d %H:%M:%S” | pbcopy` 
```

如果你用 Mac 的话也可以设置一个快捷指令来执行 Shell 脚本，然后分配一个快捷键。

更改样式
----

Pelican 默认的主题复古到令人不适。你可以在 Google 搜索 Pelican theme，或者直接去 [Pelican Themes](http://www.pelicanthemes.com/) 按图索骥，找一个自己喜欢的主题。

安装主题非常简单。一般来说你能找到的主题都托管在 GitHub 上，你可以通过 Git Submodule 来安装：

```bash
➜ git submodule add git@github.com:gilsondev/pelican-clean-blog.git
```

这里的例子是我在用的主题 [Pelican Clean Blog](https://github.com/gilsondev/pelican-clean-blog)。

Pelican 主题使用 [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) 来构建，你可以完全自己定义所有的样式。我比较懒，就直接用了原本的主题。

部署上线
----

由于 Pelican 生成的是静态文件，所以只要你有办法把 output 目录的内容复制到服务器上去，就可以部署了。

我使用的是 `rsync`。创建一个脚本：

```bash
➜ cat > deploy
#!/bin/sh
pelican
export blog_output="/path/to/your/blog/output"
export prod_dir="/serving/dir/on/your/server/"
rsync -rvz $blog_output/* user@host:$prod_dir
```

然后 `chmod +x deploy`，需要部署的时候 `./deploy` 即可。当然你也可以把它放到 git 的 post-commit hook 里。一般来讲不会有什么问题，`-v` 参数纯粹是为了部署的时候屏幕上有东西滚动看起来不那么无聊。

部署之后的效果就是你看到的样子。更详细的说明可以参考以下链接：

1.  [docs.getpelican.com](https://docs.getpelican.com/en/latest/index.html)
2.  [git-scm.com](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
3.  [linux.die.net/man/1/rsync](https://linux.die.net/man/1/rsync)