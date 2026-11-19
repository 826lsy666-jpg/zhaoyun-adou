# 赵云与阿斗 · 安卓离线版构建说明

目标：生成一个**不需要联网**的单机 APK。游戏资源、字体、存档都在手机本地。

## 没有 Linux？

先看 `NO_LINUX_ANDROID.md`：GitHub Actions、Codespaces、虚拟机、云服务器四种替代方案。

## 推荐方案：Buildozer / python-for-android

Pygame 是桌面 SDL 游戏，最稳的安卓离线方案是用 Buildozer 把 Python + Pygame + 游戏资源一起打进 APK。

注意：**Buildozer 需要 Linux 环境**。当前 Windows 上即使有 JDK/Android SDK，也不能直接运行 python-for-android；请使用 WSL2 Ubuntu、Ubuntu 虚拟机或 Linux CI。

## 一、准备 Linux/WSL2 Ubuntu

Windows 管理员 PowerShell：

```powershell
wsl --install -d Ubuntu
```

安装后重启，进入 Ubuntu 设置用户名。

在 Ubuntu 中：

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
  cmake libffi-dev libssl-dev
```

安装 Buildozer：

```bash
python3 -m venv ~/buildozer-venv
source ~/buildozer-venv/bin/activate
python -m pip install --upgrade pip
pip install buildozer cython
```

## 二、把项目复制到英文路径

Buildozer/NDK 对中文和空格路径不稳定，务必复制到英文路径：

```bash
mkdir -p ~/zyad
rsync -av \
  --exclude dist --exclude shots --exclude font_backup \
  --exclude __pycache__ --exclude build --exclude .git \
  "/mnt/e/字统三国/工作区域/赵云与阿斗/" ~/zyad/
cd ~/zyad
```

项目根目录已经包含 `buildozer.spec`。

## 三、构建离线 APK

```bash
buildozer -v android debug
```

首次构建会自动下载 Android SDK/NDK 和 Python-for-Android 工具链，约 1–2 GB，耗时 20–40 分钟。

成功后 APK 在：

```text
bin/zhaoyunadou-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

安装到手机/平板：

```bash
adb install -r bin/*.apk
```

也可以把 APK 复制到手机上，允许“安装未知来源应用”后点击安装。

## 四、确认真正离线

`buildozer.spec` 中没有 INTERNET 权限：

```ini
android.permissions =
```

安装后关闭 Wi-Fi 和移动数据，仍应能：

- 进入主菜单
- 选择关卡/无尽
- 征兵、布阵、战斗
- 保存进度
- 重启后继续读取本地存档

如需检查 APK 权限：

```bash
$ANDROID_HOME/build-tools/34.0.0/aapt dump permissions bin/*.apk
```

## 五、手机/平板适配

- `orientation = landscape`：横屏
- `fullscreen = 1`：全屏
- 游戏内部按 1600×900 逻辑画布缩放，手机/平板保持比例，四周留黑边
- 触摸事件已映射为鼠标事件
- Android 返回键映射为 Esc
- 存档目录使用 `ANDROID_PRIVATE`，无需外部存储权限

## 六、发布版签名

Debug APK 可以直接安装测试，但正式分发建议 release 签名：

```bash
keytool -genkey -v -keystore zyad.keystore -alias zyad \
  -keyalg RSA -keysize 2048 -validity 10000
buildozer -v android release
```

按 Buildozer 提示配置签名，或使用 `apksigner` 对 release APK 签名。

## 七、常见问题

- **Java 版本错误**：使用 JDK 17，不要用 JDK 8/21 混搭。
- **NDK/SDK 下载失败**：重新运行 `buildozer android clean` 后再构建。
- **pygame recipe 编译失败**：先确认 `requirements = python3,pygame`，删除 `.buildozer` 缓存后重试。
- **中文路径报错**：项目必须在 `~/zyad` 这类纯英文路径。
- **触摸坐标偏移**：确认 `fullscreen=1`，不要在 Android 上启用窗口模式。
- **存档丢失**：确认使用最新 `save.py`，它会把存档写到 `ANDROID_PRIVATE/ZhaoyunAdou`。

## 当前环境说明

这台 Windows 机器没有可用的 Linux 发行版，也没有 Buildozer。可以准备好源码和 `buildozer.spec`，但必须在 WSL2/Ubuntu/Linux 上执行最后一步 `buildozer android debug` 才能得到 APK。
