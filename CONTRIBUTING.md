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
    Open the `.env` file in Notepad. You must provide a key for a **high-quality model**.
    
    ### 🧠 AI Model Report Card
    | Model | Cost | Vision (PDFs/Images) | Logic/Reasoning | Best For... |
    | :--- | :--- | :--- | :--- | :--- |
    | **Gemini 2.0 Flash** | **FREE** | ⭐⭐⭐⭐⭐ (Native) | ⭐⭐⭐⭐ | **Most Contributors**. It can "see" PDF pages directly. |
    | **GPT-4o** | $$$ | ⭐⭐⭐ (Text Only via API) | ⭐⭐⭐⭐⭐ | Complex reasoning, but expensive. |
    | **Claude 3.5 Sonnet** | $$ | ⭐⭐⭐ (Text Only via API) | ⭐⭐⭐⭐⭐ | Excellent writer, great for extracting names. |
    
    *Update the `MODEL_NAME` in your `.env` file to switch models.*
    
    **CRITICAL**: Add your `CONTRIBUTOR_HANDLE` (e.g., `ShadowCoder`) to the file. This is how you get credit on the website!

---

## 🖥️ The Dashboard (Easiest Way)

We built a custom app to handle the hard stuff for you.

**To Launch:**
Double-click `setup.bat` again (it will launch the dashboard after checking tools), or run:
```bash
venv\Scripts\python src/dashboard.py
```

### 🛠️ How to Mine Data

### 0. 🎓 The Training Ground (Batch 000)
**First time? Start here.**
We created a "Challenge Batch" (000) so you can test your setup.

1.  Run the miner on Batch 000:
    ```bash
    python src/dossier_miner.py --batch 000
    ```
2.  Check the output in `data/processed/test_document.json`.
3.  **Did it find "The Pilot"?** Did it describe the "Black Book"?
4.  Compare your result with the community in Discord!

### 1. ✋ Claim Your Batch (IMPORTANT)
To stop two people from doing the same work, you must "check out" a batch first.
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
