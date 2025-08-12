
1. **Create GitHub repo** (visible, motivating)  
2. **Initialize local repo and connect**  
3. **Configure Git identity** (now that they’ve seen where it matters)  
4. **Generate PAT and authenticate**  
5. **Cache PAT (optional)**  
6. **Push to GitHub**  
7. **Linux commands**  
8. **`curl cheat.sh`**

---

## 📁 `090125_intro3/setup.md` — Final Refactor

```markdown
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

## [4] Generate GitHub PAT and Authenticate  
_Tag: github, auth, recovery_

### ✅ Create a Personal Access Token (PAT)
- Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
- Select scopes: `repo`, `workflow`, `read:org`
- Copy and save your token securely

> 🧠 *What Happens Next?*  
When you push to GitHub, Git will prompt you for your username and password.  
- Enter your GitHub username  
- **Paste your PAT** as the password (you won’t see it as you type)

> 💡 *Recovery Tip:* If you see `403` or `authentication failed`, regenerate your PAT and try again.

---

## [5] Cache PAT (Optional but Recommended)  
_Tag: github, credential manager_

```bash
git credential-manager-core configure
git config --global credential.helper manager-core
```

> 🎓 *Student Tip:* This caches your PAT so you won’t be prompted every time.

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
---
