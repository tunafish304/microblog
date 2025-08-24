
---

## 📁 `090125_intro3/setup.md` 
# Setup Guide — Intro Class 3 (`090125_intro3`)  
_Tag: github, linux, curl, recovery, reproducible_

This guide connects your local Git setup to GitHub, configures authentication, and introduces essential Linux commands. You’ll also learn how to use `curl cheat.sh` for fast, searchable command-line help.

---

## [1] Create GitHub Repo  
_Tag: github, reproducible, recovery_

### ✅ On GitHub:
1. Go to [https://github.com](https://github.com)
2. Click **New Repository**
3. Name it clearly (e.g., `intro3-dev-env`)
4. Leave it **empty** (no README, .gitignore, or license)

> 💡 *Recovery Tip:* If you accidentally add a README, clone the repo first and then pull before pushing.

---

## [2] Initialize Local Repo and Connect  
_Tag: git, reproducible_

### ✅ In your local project folder:
```bash
git init
git remote add origin https://github.com/your-username/intro3-dev-env.git
```

- `git remote add`: Adds a new remote connection.
- `origin`: This is just a conventional name (like a nickname) for the remote repo. You could name it anything, but `origin` is the default.
- `https://github.com/...`: The actual URL of the remote repository.
- `git push origin main` (or whatever your branch is called. In this example it's called main) will push your local commits to that remote repo.

> 🎓 *Student Tip:* Use `git status` to confirm your repo is tracking changes.

---

## [3] Configure Git Identity  
_Tag: git, reproducible_

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

> 💡 *Recovery Tip:* Use `git config --list` to verify settings.

---

## [4] GitHub Setup – Microblog Edition  
_Tag: github, auth, recovery, reproducible_

This setup gives you secure access to your microblog repo so you can push code and later clone it to PythonAnywhere.

---

### ✅ Step 1: Create Your Microblog Repo

1. Go to: [https://github.com/new](https://github.com/new)
2. Name your repo: `microblog`
3. Choose:
   - Public or private (your choice)
   - Add a README ✅
4. Click **Create repository**

---

### 🔐 Step 2: Enable Two-Factor Authentication (2FA)

GitHub requires 2FA to create a token. Set it up now so you're ready.

1. Go to: [https://github.com/settings/security](https://github.com/settings/security)
2. Click **Enable two-factor authentication**
3. Choose:
   - 📱 Authenticator app (recommended)
   - 📩 SMS (if you prefer)
4. Save your **recovery codes** somewhere safe

---

### 🔑 Step 3: Create Your Classic Token

1. Go to: [https://github.com/settings/tokens/new?type=classic](https://github.com/settings/tokens/new?type=classic)  
2. GitHub will ask for your 2FA code
3. Select these scopes:
   - ✅ `repo` (access to your microblog repo)
   - ✅ `workflow` (optional, for GitHub Actions)
4. Click **Generate token**
5. Copy your token and save it somewhere safe (you won’t see it again)

> 🎓 *Student Tip:* When Git prompts for login:
- Enter your GitHub **username**
- Paste your **token** as the password (you won’t see it as you type)

---

### 🧪 Step 4: Test Your Token (Dry Run)

Use this command to confirm your token works:

```bash
git ls-remote https://github.com/YOUR-USERNAME/microblog.git
```

If it returns a list of refs, your token is working.

> 💡 *Recovery Tip:* If GitHub blocks you or asks for 2FA and you’re stuck:
- Ask your instructor for help
- Use HTTPS with username/password temporarily
- You can always come back and finish token setup later

---

## [5] Cache PAT (Optional but Recommended)  
_Tag: github, credential manager_

```bash
git credential-manager-core configure
git config --global credential.helper manager-core
```

> 🎓 *Student Tip:* This caches your token so you won’t be prompted every time.

---

## [6] Push to GitHub  
_Tag: github, reproducible_

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

> 💡 *Recovery Tip:* If `main` doesn’t exist, rename your branch with `git branch -M main`.

---

## [7] Basic Linux Commands  
_Tag: linux, reproducible_

```bash
ls         # list files
cd         # change directory
pwd        # print working directory
mkdir      # create folder
rm         # remove file
cp         # copy file
mv         # move/rename file
```

> 🎓 *Student Tip:* Use `man <command>` for built-in help.

---

## [8] Use `curl cheat.sh` for Fast Help  
_Tag: curl, cheat.sh, reproducible_

### ✅ Syntax:
```bash
curl cheat.sh/git
curl cheat.sh/python
curl cheat.sh/bash
```

> 💡 *Recovery Tip:* If `curl` isn’t installed:
```bash
sudo apt install curl
```

> 🎓 *Student Tip:* You can search specific topics:
```bash
curl cheat.sh/python/virtualenv
```

