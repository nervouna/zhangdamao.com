Title: Flutter Startup Shows a Flashing Black Screen
Date: 2022-09-22
Slug: mysterous-black-screen-with-flutter-ios
Category: Coding
Tags: Flutter
Summary: Any bug that cannot be seen on Google, 100% is your own stupidity.

Recently, I felt that the cold start of the app was a bit strange when debugging. Upon closer inspection, I noticed that there was a brief black screen flashing after the Launch Screen disappeared and before the main interface appeared.

After searching online, I found that this has been a problem since 2019 or earlier. But after further investigation, I found that it ultimately pointed to a closed issue in the Flutter repository.

Generally, if you can’t find a search result, it’s your own problem. So I decided to use `flutter create bug` to see if there were any differences.

As a result, I found that the default project template’s Info.plist file has one difference from my implementation:

```xml
<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>
```

While in my project it was:

```xml
<key>UILaunchStoryboardName</key>
<string>LaunchScreen.storyboard</string>
```

Removing the .storyboard extension and rebuilding solved the black screen issue. 😓

When I have time, I’ll take a look at the Flutter source code and see if I can find out what the problem is.

I raised an [issue](https://github.com/flutter/flutter/issues/112160) on the Flutter repository, you can check when the development team plans to fix it.
