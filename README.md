# 📝 Microblog (Chapter 14 Baseline)

This repository contains a working implementation of **Chapter 14** from Miguel Grinberg’s Flask Mega-Tutorial. It includes foundational features like user authentication, profile pages, database models, and post creation.

## 📦 Structure Overview

- `app/`: Core application code (routes, models, forms, templates)
- `migrations/`: Database schema tracking
- `instance/`: Runtime files like SQLite DB (not tracked in Git)
- `venv/`: Python virtual environment (ignored in Git)
- `.gitignore`: Cleans up unnecessary or sensitive files
- `requirements.txt`: Project dependencies

## 🧠 Purpose

This repo serves as a **teaching baseline**—a clean, modular setup for exploring multilingual post support in upcoming chapters. All enhancements in Chapter 15 and beyond will build from this structure with minimal deviation, making it easier for learners to compare code across chapters.

## 🚀 Getting Started

To run the app locally:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
flask db upgrade
flask run