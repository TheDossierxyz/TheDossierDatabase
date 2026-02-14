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
    Open the `.env` file in Notepad. You must provide a key for a model.
    `CONTRIBUTOR_HANDLE=YourAliasHere` (Do NOT use your real name for privacy).

    ### 🧠 AI Model Report Card (2025 Update)

    | Model | Cost (per 1M tokens) | Native PDF Support | Logic / Reasoning | Best For... |
    | :--- | :--- | :--- | :--- | :--- |
    | **Gemini 2.0 Flash** | **FREE** (AI Studio) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **The Standard.** Best for most contributors. High speed and "sees" layout perfectly. |
    | **GPT-4o** | $2.50 in / $10 out | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Complex Documents.** Best for messy layouts, handwriting, or high-stakes logic. |
    | **Claude 3.5 Sonnet** | $3.00 in / $15 out | ⭐⭐⭐⭐ (Beta) | ⭐⭐⭐⭐⭐ | **Data Formatting.** Best at strict "JSON" output and extracting names without typos. |
    | **GPT-4o mini** | $0.15 in / $0.60 out | ⭐⭐⭐⭐ | ⭐⭐⭐ | **Bulk Processing.** Extremely cheap. Use for thousands of simple, clear text PDFs. |
    | **Llama 3.2 Vision** | $ (Varies) | ⭐⭐⭐ (via Image) | ⭐⭐⭐ | **Open Source.** Good for users running local AI (Ollama) or using Groq. |
    | **Mistral OCR** | - | ⭐⭐⭐⭐⭐ | N/A | **The Specialist.** Specializes in reading complex tables. |

    ### 📋 Detailed Guide for Your Users

    **1. The "Free & Fast" Path (Gemini 2.0 Flash)**
    *   **How to get it**: Get a key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   **Why use it**: Huge "context window" (100+ page PDFs) and free for standard use.
    *   *Pro Tip*: Best sustainable choice for volunteers.

    **2. The "Accuracy First" Path (GPT-4o)**
    *   **How to get it**: Get a key from [OpenAI Platform](https://platform.openai.com/api-keys).
    *   **Why use it**: Industry leader in visual "transcription" for handwriting/stamps.
    *   *Pro Tip*: Expensive ($5–$15 per 100 pages), use only on difficult documents.

    **3. The "Strict Format" Path (Claude 3.5 Sonnet)**
    *   **How to get it**: Get a key from [Anthropic Console](https://console.anthropic.com/).
    *   **Why use it**: "Lazy-proof". Excellent at strict JSON and complex table rows.
    *   *Pro Tip*: Use for very specific, complex JSON formats.

    **4. The "Local / Privacy" Path (Llama 3.2 via Ollama)**
    *   **How to get it**: Download [Ollama](https://ollama.com/) (No key required).
    *   **Why use it**: For sensitive data or processing millions of pages without a bill.

---

## 🖥️ The Dashboard (Easiest Way)

We built a custom app to handle the hard stuff for you.

**To Launch:**
Double-click `setup.bat` again, or run:
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
1.  **Enter Batch ID**: "Claims" the folder name from `data/raw_batches` (e.g. `001`).
2.  **Click "✋ Claim Batch"**: This locks it so nobody else takes it.
3.  **Click "⛏️ Start Mining"**: The AI will start reading files. Watch the logs!
4.  **Click "🚀 Submit Work"**: Sends your data to the database.

---

## 🤓 Advanced (Command Line)

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
