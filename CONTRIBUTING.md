# Contributing to The Dossier Database

Thank you for helping us build the world's most comprehensive community-driven database.

## 🚀 Quick Start (Windows)

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/TheDossierxyz/TheDossierDatabase.git
    cd TheDossierDatabase
    ```

2.  **Run Setup**:
    Double-click `setup.bat`.
    *   This installs everything.
    *   It creates your `.env` file.

3.  **Add Your Keys**:
    Open `.env` in Notepad. Add your **Gemini 2.0**, **GPT-4o**, or **Claude** key.

---

## 🖥️ The Dashboard (Easiest Way)

We built a custom app to handle the hard stuff for you.

**To Launch:**
Double-click `setup.bat` again (it will launch the dashboard after checking tools), or run:
```bash
venv\Scripts\python src/dashboard.py
```

### How to use the Dashboard:
1.  **Enter Batch ID**: Pick a folder name from `data/raw_batches` (e.g. `001`).
2.  **Click "✋ Claim Batch"**: This locks it so nobody else takes it.
3.  **Click "⛏️ Start Mining"**: The AI will start reading files. Watch the logs!
4.  **Click "🚀 Submit Work"**: Sends your data to the database.

---

## 🤓 Advanced (Command Line)

If you prefer the black terminal screen:

### 1. Claim
```bash
python src/claim_batch.py --batch 001
git pull && git add claims/ && git commit -m "Claim 001" && git push
```

### 2. Mine
```bash
python src/dossier_miner.py --batch 001
```

### 3. Submit
```bash
git add data/processed
git commit -m "Processed 001"
git push
```

## Need Help?
Check out [COMMUNITY.md](COMMUNITY.md) for Discord/Telegram links!
