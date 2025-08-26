

# 🧰 VS Code Teaching Kit Setup (WSL + Python + Git)

Welcome! This guide walks you through setting up your coding environment using VS Code, WSL (Windows only), Python, Git, and a few key extensions. Follow each step carefully, and don’t worry — if something doesn’t look exactly like this, we’ll help you recover.

---

## 📦 Installation Overview: macOS vs Windows

Use this table to see what you need to install based on your operating system.

| Tool                  | macOS                                                                 | Windows 11                                                                 |
|-----------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Python**            | Already installed (`python3 --version`) <br> If missing: [Download](https://www.python.org/downloads/mac-osx/) | [Download](https://www.python.org/downloads/windows/) <br> ✅ Add to PATH during install |
| **VS Code**           | [Download](https://code.visualstudio.com/) <br> Drag to Applications | [Download](https://code.visualstudio.com/) <br> Installer handles PATH setup |
| **Git**               | Already installed <br> If missing: `brew install git` (requires Homebrew) | [Download Git](https://git-scm.com/download/win) <br> ✅ Installs at system level |
| **WSL**               | Not needed                        | Run in PowerShell as Admin:<br>`wsl --install`<br>✅ Reboot required |
| **VS Code Extensions**| Use GUI: `Ctrl+Shift+X` → Search & Install | Same as macOS |
| **VS Code Settings**  | Use `.vscode/settings.json` inside your project folder | Same as macOS |

---

## 🧱 Setting Up WSL (Windows Only)

If you're on Windows, you'll need to install WSL (Windows Subsystem for Linux). Here's how to do it:

### 🔧 Step 1: Run the Install Command

Open **PowerShell as Administrator** and type:

```powershell
wsl --install
```

You’ll see messages like:

```
Installing: WSL
Installing: Ubuntu
Downloading…
Installing…
```

Let it run — this part can take a few minutes.

---

### 🔄 Step 2: Reboot When Prompted

When the install finishes, you’ll see:

```
The requested operation is successful. Changes will not be effective until the system is rebooted.
```

Go ahead and restart your computer. This is required to finish the setup.

---

### 🖥️ Step 3: First Boot (Ubuntu Setup)

After rebooting, Windows will automatically launch a terminal window. You’ll see:

```
Installing, this may take a few minutes...
Please create a user account.
```

This means Ubuntu is finishing its setup. You’re almost there.

---

### 👤 Step 4: Create Your Linux Username & Password

Next, you’ll be prompted to enter:

```
Enter new UNIX username:
```

Type a short name (like `alex`, `student1`, or your first name). Then you’ll be asked to set a password:

```
Enter new UNIX password:
Retype new UNIX password:
```

You won’t see the password as you type — that’s normal. Just type it carefully both times.

✅ This account is your Linux identity inside WSL. You’ll use it when installing packages or running commands.

---

### 🧪 Step 5: Confirm You’re Inside Ubuntu

After you enter your password and hit return, Ubuntu finishes setting up and drops you into your Linux shell. You’ll see a prompt like this:



```bash
student1@DESKTOP-XXXX:~$
```

This means you’re inside Ubuntu and ready to go.

---

### 🐍 Step 6: Install Python (if needed)

Type:

```bash
python3 --version
```

If you see something like `Command 'python3' not found`, run:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

This installs Python and pip inside Ubuntu. You’ll be using this Python environment for your projects.

---

## 🔌 Install VS Code Extensions (GUI Only)

Now that VS Code is installed, let’s add the extensions you’ll need. Open VS Code and press `Ctrl+Shift+X` to open the Extensions tab. Then search for each extension below and click **Install**.

| Extension Name                     | What It Does                                  |
|-----------------------------------|-----------------------------------------------|
| **Remote - WSL**                  | Connect VS Code to WSL (Windows only)         |
| **GitHub Copilot**                | AI code suggestions                           |
| **GitHub Copilot Chat**           | Chat-based coding assistant                   |
| **GitHub Pull Requests and Issues** | GitHub integration for PRs and issues        |
| **Python Indent**                 | Smart indentation for Python                  |
| **Black Formatter**               | Auto-format Python code                       |
| **Debugpy**                       | Python debugging support                      |
| **Python**                        | Core Python extension                         |
| **Pylance**                       | Fast Python language server                   |
| **Python Environments**           | Manage Python virtual environments            |
| **Live Server**                   | Preview HTML/CSS/JS in browser                |

💡 If your project folder includes a `.vscode/extensions.json` file, VS Code will prompt you to install any missing extensions automatically.

---

## ⚙️ VS Code Settings

Inside your project folder, create a `.vscode/` folder and add a file called `settings.json`. Paste the following into it:

```json
{
  "editor.tabSize": 4,
  "editor.insertSpaces": true,

  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,

  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,

  "git.enableSmartCommit": true,
  "git.confirmSync": false,

  "liveServer.settings.port": 5500,

  "extensions.ignoreRecommendations": false
}
```

This file helps VS Code remember your preferences and automatically configure your environment when you open the folder.

---

## 📄 Optional: Extension Recommendations

You can also add a file called `extensions.json` inside your `.vscode/` folder. This helps VS Code prompt you to install any missing extensions when you open the project.

```json
{
  "recommendations": [
    "ms-vscode-remote.remote-wsl",
    "github.copilot",
    "github.copilot-chat",
    "github.vscode-pull-request-github",
    "kevinrose.vsc-python-indent",
    "ms-python.black-formatter",
    "ms-python.debugpy",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.vscode-python-envs",
    "ritwickdey.liveserver"
  ]
}
```

---

## 🧪 Recovery & Reset Tips

If something breaks or doesn’t look right, feel free to freak out, and then we'll work to find out what went wrong and fix it.