
- 🐍 Python3 and pip3 inside WSL  
- 🧪 Creating and activating `venv`  
- 📦 Managing `requirements.txt`  
- 🔁 Git basics and undo commands  
- 🧠 Recovery modeling and student-facing clarity  

---

## ✅ Scaffolding `082725_intro2/setup.md`

```markdown
# Setup Guide — Intro Class 2 (`082725_intro2`)
_Tag: python, venv, pip, git, reproducible, recovery_

This guide builds on your environment from Intro Class 1. You’ll set up a virtual environment, install packages, manage dependencies, and learn Git basics—including how to undo common mistakes.

---

## [1] Verify Python3 and pip3 in WSL  
_Tag: python, reproducible_

Run inside WSL:
```bash
python3 --version
pip3 --version
```

> 💡 *Recovery Tip:* If `python3` or `pip3` not found, run:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## [2] Create and Activate Virtual Environment  
_Tag: venv, reproducible, recovery_

Inside your project folder:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> 🎓 *Student Tip:* You don’t need `venv` until you start installing packages. We introduce it here so your environment stays isolated and reproducible.

> 💡 *Recovery Tip:* If `source` fails, check that `.venv` exists and retry `python3 -m venv .venv`.

---

## [3] Install Packages with pip  
_Tag: pip, reproducible_

Example:
```bash
pip install flask
```

---

## [4] Create and Manage `requirements.txt`  
_Tag: dependencies, reproducible_

### ✅ Create from current environment:
```bash
pip freeze > requirements.txt
```

### ✅ Install from file:
```bash
pip install -r requirements.txt
```

### ✅ Add manually:
Edit `requirements.txt` and run:
```bash
pip install -r requirements.txt
```

> 💡 *Recovery Tip:* If install fails, check for typos or incompatible versions.

---

## [5] Git Basics  
_Tag: git, reproducible, recovery_

### ✅ Common Commands:
```bash
git init
git status
git add .
git commit -m "Initial commit"
git log
```

### 🔁 Undo Mistakes:
- Undo last commit (keep changes):  
  ```bash
  git reset --soft HEAD~1
  ```
- Unstage a file:  
  ```bash
  git restore --staged filename.py
  ```
- Discard changes:  
  ```bash
  git checkout -- filename.py
  ```

> 🎓 *Student Tip:* Git lets you recover from most mistakes. Practice undoing safely before pushing to GitHub.

---

## ✅ Next: `090125_intro3/setup.md`  
You’ll configure GitHub, cache your PAT, and explore Linux commands and curl cheat.sh.

```

---