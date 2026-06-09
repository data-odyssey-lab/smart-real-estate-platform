# Contributing Guide

## Environment Setup

This project uses a shared Python virtual environment.

### First Time Setup
```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### When You Install New Packages
```bash
pip freeze > requirements.txt
```
Then commit the updated requirements.txt. Never commit the venv/ folder.

## Branch Naming
- ML team: ml-and-training
- DE team: #pending
- Analytics: #pending

## Pull Requests
Always open a PR to main - never push directly to main.
