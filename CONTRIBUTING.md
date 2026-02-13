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
    *   This will install all dependencies.
    *   It will create a `.env` file for you.

3.  **Add Your Keys**:
    Open the `.env` file in Notepad. You must provide a key for a **high-quality model**.
    
    *   **Gemini 2.0 Flash (Recommended)**: [Get Key](https://aistudio.google.com/app/apikey)
    *   **OpenAI GPT-4o**: [Get Key](https://platform.openai.com/api-keys)
    *   **Claude 3.5 Sonnet**: [Get Key](https://console.anthropic.com/)
    
    Update the `MODEL_NAME` in .env if you are not using the default (gemini-2.0-flash).

---

## 🛠️ How to Mine Data

### 1. ✋ Claim Your Batch (IMPORTANT)
To stop two people from doing the same work, you must "check out" a batch first.

```bash
venv\Scripts\activate
# Replace 001 with the folder name you want to work on
python src/claim_batch.py --batch 001
```

If it says **[SUCCESS]**, you must verify the lock immediately:
```bash
git pull origin main  # Get latest claims
git add claims/
git commit -m "Claim batch 001"
git push origin main
```
*If the push fails, someone else claimed it first. Pull again and pick another batch.*

### 2. Run the Miner
Once you have successfully pushed your claim, run the miner:

```bash
python src/dossier_miner.py --batch 001
```

### 3. Submit Your Work
Push your processed data to GitHub and open a Pull Request!
```bash
git add data/processed
git commit -m "Processed batch 001"
git push origin main
```

---

## ✅ The Rules (Automated Validation)

We use an automated "Bouncer" script. Your submission **will be rejected** if:
1.  **Invalid JSON**: The format must be perfect.
2.  **Hallucinations**: Every connection must have a `quote` that physically exists in the document text.
3.  **Broken Links**: You cannot link to an Entity ID that doesn't exist in the `entities` list.

Thank you for contributing!
