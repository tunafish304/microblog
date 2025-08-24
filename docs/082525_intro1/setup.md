
# Setup Guide — Intro Class 1 (`082525_intro1`)
_Tag: setup, onboarding, reproducible, recovery_

Welcome! This guide prepares your development environment for the course. Each step is modular, annotated, and designed to help you recover gracefully if something goes wrong.

---

## [1] Install Global Python (≥3.11)  
_Tag: python, path, reproducible_

  ✅ Download: [https://www.python.org/downloads](https://www.python.org/downloads)
- ✅ On the first page of the installer make sure "Add to PATH" is checked and then proceed through the installer steps and complete the installation
- ✅ Verify PATH:  
  ```bash
  python --version
  where python
  ```
- 🔁 Recovery: If `python` not found, revisit installer and ensure "Add to PATH" is checked.

---

## [2] Install WSL (Windows Subsystem for Linux)  
_Tag: environment, reproducible, recovery_

WSL lets you run a Linux environment inside Windows. For most students, WSL2 will be installed automatically. If your system doesn’t support WSL2, Windows will silently fall back to WSL1—which is fully supported for this course.

### ✅ Install WSL
Open PowerShell as Administrator:
```powershell
wsl --install
```

### ✅ Verify WSL Version
```bash
wsl --list --verbose
```

> 🎓 *Student Tip:* WSL1 is perfectly fine for this course. You won’t notice any difference unless you're using Docker or advanced Linux features.

### 🔁 Recovery: If WSL Hangs
```bash
wsl --shutdown
```

---

## [3] Install VS Code  
_Tag: editor, reproducible_

- ✅ Download: [https://code.visualstudio.com](https://code.visualstudio.com)
- Open the installer and go through the install steps

---

## [4] Install VS Code Extensions  
_Tag: extensions, reproducible, recovery_

### Recommended Extensions (CLI install):
```bash
# Recommended install order for VS Code extensions

# 1. WSL integration
code --install-extension ms-vscode-remote.remote-wsl

# 2. Core Python stack
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.vscode-python-envs
code --install-extension ms-python.debugpy
code --install-extension ms-python.black-formatter
code --install-extension kevinrose.vsc-python-indent

# 3. Copilot tools
code --install-extension github.copilot
code --install-extension github.copilot-chat

# 4. GitHub PR extension
code --install-extension github.vscode-pull-request-github

# 5. Live Server (optional for HTML)
code --install-extension ritwickdey.liveserver
```

> 💡 *Recovery Tip:* If extensions fail to install, try launching VS Code as admin or reinstalling.

---

## [5] Check for Extension Conflicts  
_Tag: recovery, reproducible_

- ✅ Open VS Code → `Help > Toggle Developer Tools` → check console for extension errors
- ✅ Disable conflicting extensions via `Extensions > Installed > Disable`

---

## [6] Apply Recommended `settings.json`  
_Tag: reproducible, config_
 
- Use Ctrl+Shft+P to get to the Command Paletter
- In the drop down list find Preferences: Open User Settings (JSON)
- Your settings.json file should look like the following json:
```json
{
  "terminal.integrated.defaultProfile.windows": "Ubuntu (WSL)",
  "workbench.colorTheme": "GitHub Light High Contrast",
  "workbench.startupEditor": "none",
  "[python]": {
    "editor.formatOnType": true,
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "always",
      "source.organizeImports": "always"
    }
  },
  "terminal.integrated.defaultProfile.linux": "bash",
	"python.terminal.activateEnvironment": true, 
  "python.terminal.activateEnvInCurrentTerminal": true,
  "remote.autoForwardPortsSource": "hybrid",
  
	// Optional: Only set if the venv isn't directly in your workspace folder
	// "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```
> 💡 *Recovery Tip:* If settings don’t apply, restart VS Code or check for syntax errors in `settings.json`.

---