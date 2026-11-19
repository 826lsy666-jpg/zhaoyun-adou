[app]
title = 赵云与阿斗
package.name = zhaoyunadou
package.domain = com.zyad

source.dir = src
source.include_exts = py,png,jpg,jpeg,ttf,ico
source.exclude_dirs = __pycache__, tests
version = 1.0.0

# 纯离线：不加 INTERNET 权限
requirements = python3,pygame
orientation = landscape
fullscreen = 1
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a,armeabi-v7a
android.permissions =
android.allow_backup = True
android.accept_sdk_license = True
android.apptheme = @android:style/Theme.NoTitleBar.Fullscreen
icon.filename = %(source.dir)s/zyad/assets/icon.png
p4a.bootstrap = sdl2
android.debug_artifact = apk
android.release_artifact = apk
