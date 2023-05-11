Title: 踩坑：Flutter 启动闪现黑屏
Date: 2022-09-22
Category: 编程
Tags: Flutter

最近调试的时候总觉得 app 冷启动怪怪的，仔细看发现在 Launch Screen 消失后、主界面出现前有一个一闪而过的黑屏。

在网上搜索了一下，发现这是一个自 2019 年（或更早）就存在的问题。但是追了一下搜索结果，发现最终指向 flutter 仓库里的某个 close 掉的 issue。

一般来说，搜索不到的问题就是自己的问题。于是我决定 `flutter create bug` 看看有什么不同。

结果发现默认项目模板里的 `Info.plist` 有一处和我的写法不同：

```xml
<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>
```
而我的项目里则是：

```xml
<key>UILaunchStoryboardName</key>
<string>LaunchScreen.storyboard</string>
```
去掉了 `.storyboard` 拓展名，重新编译运行，黑屏消失了😓

等有空的时候看看 flutter 源码，看看能不能找到是什么问题。

给 flutter repo 提了一个 [issue](https://github.com/flutter/flutter/issues/112160)，看看啥时候开发组打算修复。