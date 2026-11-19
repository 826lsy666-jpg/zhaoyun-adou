# 没有 Linux 时怎么生成安卓 APK

目标：不在这台 Windows 上安装 Linux，也能得到可离线运行的 APK。

推荐顺序：

1. **GitHub Actions 云端 Ubuntu**：最省事，免费额度够，浏览器操作
2. **GitHub Codespaces**：浏览器里的 Linux 终端，适合边看边改
3. **本机虚拟机 Ubuntu**：完全本地，但需要 VirtualBox/VMware 和虚拟化
4. **云服务器 Ubuntu**：最可控，需要一台 Linux VPS

Buildozer / python-for-android 不能在 Windows 原生运行；下面都是绕过这一点的方法。

---

## 方案一：GitHub Actions（推荐，不需要本机 Linux）

项目里已经带了工作流：

```text
.github/workflows/android.yml
```

### 1. 准备 GitHub 账号

没有账号就到 https://github.com 注册，免费账号即可。

### 2. 把项目上传到 GitHub

最省事的是安装 **GitHub Desktop**（Windows 图形界面，不需要命令行）：

1. 安装 GitHub Desktop：https://desktop.github.com/
2. 登录 GitHub 账号
3. 为了避免中文路径问题，先把项目复制到英文路径，例如：

   ```text
   E:\zyad_android
   ```

   复制内容至少包括：

   ```text
   buildozer.spec
   src\
   .github\
   README.md
   ```

   不需要复制 `dist`、`shots`、`font_backup`、`build`、`__pycache__`。

4. GitHub Desktop → File → Add local repository
   - 选择 `E:\zyad_android`
   - 如果提示不是 Git 仓库，点 **create a repository**
   - Name：`zhaoyun-adou`
   - Local path：`E:\zyad_android`
   - 点 Create repository
5. 填写 commit message，点 **Commit to main**
6. 点 **Publish repository**
   - Public：Actions 免费额度无限，推荐
   - Private：免费账号每月约 2000 分钟，构建一次通常 30–60 分钟

### 3. 运行云端构建

1. 打开 GitHub 仓库页面
2. 点 **Actions**
3. 左侧选择 **Build Android APK**
4. 点 **Run workflow** → 选择 `main` → **Run workflow**
5. 等待构建完成（首次 30–60 分钟，之后有缓存会快一些）

构建步骤会自动：

- 安装 JDK 17
- 安装 Buildozer
- 下载 Android SDK/NDK
- 执行 `buildozer -v android debug`
- 上传 APK 为 Actions artifact

### 4. 下载 APK

在完成的 workflow 页面底部：

```text
Artifacts
  zhaoyun-adou-apk
```

点击下载 zip，解压后得到：

```text
zhaoyunadou-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

把 APK 传到手机/平板安装即可。

### 5. 更新版本

以后改了游戏代码：

1. GitHub Desktop 提交并 Push
2. Actions 里的 workflow 会自动触发，也可以手动 Run workflow
3. 重新下载 artifact

### 常见失败

- **Buildozer 下载超时**：重新 Run workflow；缓存会让第二次更快
- **NDK/SDK 空间不足**：GitHub 免费 runner 一般够用；失败时看日志里具体包
- **Java 版本**：工作流已固定 JDK 17
- **buildozer.spec 找不到**：确认文件在仓库根目录
- **APK 产物为空**：看 Build 日志最后的错误，通常是 pygame recipe 或 NDK 下载

---

## 方案二：GitHub Codespaces（浏览器里的 Ubuntu）

适合不想配置本机、又想手动执行命令的情况。

1. 按方案一把项目上传 GitHub
2. 仓库页面 → **Code** → **Codespaces** → **Create codespace on main**
3. 在浏览器 VS Code 的 Terminal 里执行：

   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
     autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
     cmake libffi-dev libssl-dev

   python3 -m venv ~/buildozer-venv
   source ~/buildozer-venv/bin/activate
   pip install --upgrade pip buildozer cython

   cd /workspaces/zhaoyun-adou
   buildozer -v android debug
   ```

4. 构建完成后，在左侧文件树找到：

   ```text
   bin/*.apk
   ```

   右键 Download 下载到本机。

Codespaces 免费额度通常每月 60 小时、15 GB 存储；Android SDK/NDK 会占空间，建议构建完删除 `.buildozer` 缓存。

---

## 方案三：本机虚拟机 Ubuntu（完全本地）

适合不想把代码传到 GitHub 的情况。

1. 安装 **VirtualBox** 或 **VMware Workstation Player**
2. 下载 **Ubuntu 22.04 Desktop ISO**
3. 新建虚拟机：
   - 内存 4 GB 以上
   - 磁盘 30 GB 以上
   - 开启虚拟化（BIOS 里 VT-x/AMD-V）
4. 安装 Ubuntu
5. 在虚拟机里安装构建依赖：

   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
     autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
     cmake libffi-dev libssl-dev

   python3 -m venv ~/buildozer-venv
   source ~/buildozer-venv/bin/activate
   pip install --upgrade pip buildozer cython
   ```

6. 把项目复制进虚拟机，**必须放在英文路径**，例如：

   ```bash
   mkdir -p ~/zyad
   # 通过共享文件夹/拖拽把项目复制到 ~/zyad
   cd ~/zyad
   buildozer -v android debug
   ```

7. 从 `~/zyad/bin/` 把 APK 复制回 Windows。

缺点：首次下载 Ubuntu、Android SDK/NDK 较大；虚拟机性能较低。

---

## 方案四：Linux 云服务器

适合有云服务器或愿意买一台最便宜 VPS 的情况。

1. 购买 Ubuntu 22.04 VPS（1–2 GB 内存即可，磁盘 25 GB+）
2. SSH 登录
3. 安装依赖和 Buildozer（命令同方案三）
4. 把项目上传：

   ```bash
   scp -r "E:\zyad_android" user@服务器IP:~/
   ```

   或使用 GitHub 拉取
5. 构建：

   ```bash
   cd ~/zyad_android
   buildozer -v android debug
   ```

6. 下载 APK：

   ```bash
   scp user@服务器IP:~/zyad_android/bin/*.apk .
   ```

注意：不要在服务器上长期保留 `.buildozer`/SDK 缓存，占用空间较大。

---

## 不推荐的方案

### 1. Windows 直接安装 Buildozer

Buildozer/python-for-android 依赖 Linux 工具链；Windows 原生环境不受支持。MSYS2/Cygwin 也不是官方支持路径。

### 2. 随机在线 APK 转换器

不支持 Pygame，无法把 Python/SDL 游戏正确打包，且有安全风险。

### 3. WebView/Pygbag 离线包

理论可行，但需要额外处理 Python WASM、pygame wheel、COOP/COEP 和 WebView 本地资源加载；比 Buildozer 更容易出兼容问题，不作为首选。

---

## 构建完成后确认离线

安装 APK 后：

1. 打开飞行模式
2. 启动「赵云与阿斗」
3. 进入关卡、征兵、布阵、战斗
4. 退出再进入，确认存档仍在

`buildozer.spec` 没有 INTERNET 权限；游戏资源、字体、存档都在本地。

---

## 文件位置

- 构建配置：`buildozer.spec`
- 云端工作流：`.github/workflows/android.yml`
- 常规 Android 构建说明：`ANDROID.md`
