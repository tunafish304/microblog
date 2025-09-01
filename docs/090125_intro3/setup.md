## For Mac users - Step 0
```bash
mkdir -p ~/projects/microblog
cd ~/projects/microblog
```
---
## Step 1 - start vs code
**NOTE:** Windows users only: Open Powershell (you don't need administrator privileges) and run the following commands:

<br>

```bash
code --install-extension ms-vscode-remote.remote-wsl
wsl ~ #this will take you to your home directory in wsl
cd ~/projects/microblog
```
From the microblog directory (all users):
```bash
code .
```
---
## Step 2 - create the file settings.json
**NOTE:** *Make sure the file name **settings.json** is all lower case*
<br>1. Type the following commands at the vs code terminal (make sure you are in the microblog folder)

```bash
mkdir .vscode
cd .vscode
touch settings.json #this will create the settings.json file
```
<br>
2. Open ~/projects/microblog/.vscode/settings.json file in the vs code editor and copy and paste these settings into it:

```json
{
  //Mac users can ignore the `defaultProfile.windows` setting
  "terminal.integrated.defaultProfile.windows": "Ubuntu (WSL)",
  "terminal.integrated.defaultProfile.linux": "bash",
  "workbench.startupEditor": "none",
  "workbench.colorTheme": "Default Light Modern",

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

  "python.terminal.activateEnvironment": true,
  "python.terminal.activateEnvInCurrentTerminal": true,
  "remote.autoForwardPortsSource": "hybrid",
  "github.copilot.nextEditSuggestions.enabled": true,

  // Optional: Uncomment if venv is outside workspace root
  // "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```
## Step 3 - Create and run the cross platform extensions script
<br>
1. In the microblog folder inside the vs code terminal:
<br>

```bash
touch install_extensions.sh
```
<br>
2. Inside the vs code editor, paste the contents of the script below into<br>
~/projects/microblog/install_extensions.sh

<br>

```bash
#!/bin/bash

# ┌────────────────────────────────────────────┐
# │ VS Code Extension Installer                │
# └────────────────────────────────────────────┘
# Installs essential VS Code extensions for Python development.
# Safe to run multiple times (idempotent).

# ─── Dry-run safety ──────────────────────────
set -e  # Exit on error
trap 'echo "Something went wrong. Try rerunning or ask for help."' ERR

# ─── Shared Extensions ───────────────────────
SHARED_EXTENSIONS=(
  ms-python.python
  ms-python.vscode-pylance
  ms-toolsai.jupyter
  ms-python.black-formatter
  ms-python.debugpy
  ms-python.vscode-python-envs
  github.copilot
  github.copilot-chat
  github.vscode-pull-request-github
  kevinrose.vsc-python-indent
)

# ─── Install Function ────────────────────────
install_extensions() {
  for ext in "${@}"; do
    echo "Installing: $ext"
    code --install-extension "$ext" || echo "Already installed or failed: $ext"
  done
}

# ─── Run Installer ───────────────────────────
install_extensions "${SHARED_EXTENSIONS[@]}"

```
<br>
3. Run the script by typing the following at the vs code terminal in the microblog folder:

---
Run install_extensions.sh:
```bash
chmod +x install_extensions.sh
bash install_extensions.sh
```
## Step 4: Create a GitHub Account
If you don’t have one:
- Go to [github.com](https://github.com)
- Click **Sign Up**
- Choose a username, email, and password
- Verify your email

---

## Step 5: Create a New Repository
1. Log into GitHub
2. Click the **+** icon (top-right) → **New repository**
3. Name it `microblog`
4. Choose:
   - **Public**
   - **No README**, **No .gitignore**, **No license**
5. Click **Create repository**

> This gives you a clean repo URL like:  
`https://github.com/<your-username>/microblog.git`

---

## Step 6: Enable Two-Factor Authentication (2FA) with Authenticator App

1. **Go to GitHub Settings**
   - Click your profile picture (top-right) → **Settings**
   - In the left sidebar, click **Password and authentication**

2. **Start 2FA Setup**
   - Click **Enable two-factor authentication**
   - Choose **Set up using an app**

3. **Install an Authenticator App (if needed)**
   - Recommended apps:
     - [Microsoft Authenticator](https://www.microsoft.com/en-us/security/mobile-authenticator-app)
     - [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
     - [Authy](https://authy.com/)
   - Download and install the app on your phone

4. **Scan the QR Code**
   - On GitHub, you’ll see a QR code
   - Open your authenticator app
   - Tap **Add account** or **+**
   - Choose **Scan QR code**
   - Point your phone’s camera at the QR code on your screen

5. **Enter the 6-digit Code**
   - Your app will now show a 6-digit code that refreshes every 30 seconds
   - Type that code into GitHub to verify

6. **Save Your Recovery Codes**
   - GitHub will give you a set of backup codes
   - Save them in a safe place (e.g., password manager or printed copy)

> Once set up, you’ll use the authenticator app to verify your identity when logging in or generating tokens.

---

## Step 7: Create a Fine-Grained Token
1. Go to [GitHub Tokens](https://github.com/settings/tokens)
2. Click **Generate new token (fine-grained)**
3. Name it `microblog-token`
4. Set expiration (e.g., 30 days)
5. Under **Repository access**, choose:
   - **Only select repositories**
   - Select your `microblog` repo
6. Under **Permissions**, enable:
   - **Contents: Read and write**
7. Click **Generate token**
8. **Copy the token** immediately

---

## Step 8: Initialize Git
1. In the microblog folder in vs code run this command in the terminal:
```bash
git init
```
---

## Step 9: Configure Git (One-Time Setup)
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global init.defaultBranch main
git config --global credential.helper store
```

---

## Step 10: Connect to GitHub Repo
Replace `<your-username>` with your actual GitHub username:
```bash
git remote add origin https://github.com/<your-username>/microblog.git
```

---

## Step 11: Add files and Push
1. echo "# Microblog Project" > `README.md`
2. touch `.gitignore` 
3. Add content to `.gitignore` in the vs code editor:

```
.vscode/
__pycache__/
*.pyc
.env
```

4. Save `.gitignore`in the vs code editor
5. In the terminal, add, commit and push:
```bash
git add README.md
git commit -m "Initial commit"
git push origin main
```
6. When prompted:
   - Enter your **GitHub username**
   - Paste your **token** as the password

---
## Note:
If you get an error after pushing or pasting your token, make sure you are pasting your **token** and not your **password**, and make sure the branch is named main and not master:

- Check current branch name:
git branch

- Rename if needed:
git branch -m master main

When you first create a repo, GitHub shows a setup page with helpful commands. Once you push your first commit, it transforms into the regular repo view. That’s your signal that everything’s wired up correctly.

---


## Basic Linux Commands we'll use at first: 


```bash
ls         # list files
cd         # change directory
pwd        # print working directory
mkdir      # create folder
rm         # remove file
cp         # copy file
mv         # move/rename file
```
---

## Use `curl cheat.sh` for Fast Help 

### Syntax:
```bash
curl cheat.sh/ls         # list files
curl cheat.sh/cd         # change directory
curl cheat.sh/pwd        # print working directory
curl cheat.sh/mkdir      # create folder
curl cheat.sh/rm         # remove file
curl cheat.sh/cp         # copy file
curl cheat.sh/mv         # move/rename file
```
### For help with git commands:

Install tldr:
```
sudo apt update
sudo apt install tldr
```
To see info about the "add" command for example:
```
tldr git add
```