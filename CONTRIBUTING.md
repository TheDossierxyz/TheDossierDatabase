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
    Open the `.env` file in Notepad and paste your API key.
    *   **Gemini (Free)**: [Get Key Here](https://aistudio.google.com/app/apikey)
    *   **OpenAI**: [Get Key Here](https://platform.openai.com/api-keys)
    *   Also add your `CONTRIBUTOR_HANDLE` so we can credit you!

---

## 🛠️ How to Mine Data

### 1. Claim a Batch
Check the `data/raw_batches` folder. Pick a subfolder that hasn't been processed yet.

### 2. Run the Miner
Open your terminal (Command Prompt or PowerShell) and run:

```bash
# Activate the environment (if not already active)
venv\Scripts\activate

# Run the miner on your specific batch folder
python src/dossier_miner.py --batch my_batch_folder_name
```

The script will:
*   Read each file in the batch.
*   Extract entities and connections using the AI.
*   Validate the output against our strict schema.
*   Save the clean JSON to `data/processed/`.

### 3. Submit Your Work
Push your changes to GitHub and open a Pull Request!
```bash
git add data/processed
git commit -m "Processed batch my_batch_folder_name"
git push origin main
```

---

## ✅ The Rules (Automated Validation)

We use an automated "Bouncer" script. Your submission **will be rejected** if:
1.  **Invalid JSON**: The format must be perfect.
2.  **Hallucinations**: Every connection must have a `quote` that physically exists in the document text.
3.  **Broken Links**: You cannot link to an Entity ID that doesn't exist in the `entities` list.

Thank you for contributing!
