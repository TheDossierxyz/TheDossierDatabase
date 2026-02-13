# The Dossier Database

**A decentralized, community-driven knowledge graph of public interest data.**

Our mission is to convert unstructured documents (PDFs, emails, reports) into a structured graph database (Neo4j) that anyone can query.

## 📂 Project Structure

*   `data/raw_batches/`: Source documents waiting to be processed.
*   `data/processed/`: Structured JSON files extracted by contributors.
*   `src/`: Tools for mining and validation.
*   `schema.json`: The "Ironclad" contract that defines our data structure.

### 🔍 The "Gold Standard" Example

This is why our schema is strict. We turn raw text into perfect data.

**Raw Text:**
> Sent: Tue 5/30/2017 12:05 PM
> To: [BLACKED OUT]
> From: Lesley Groff
> Subject: Re: Snacks at noon with Maxim and his mom?
> Do you want snacks at the noon appt today with Maxim and his mom?

**Extracted JSON:**
```json
{
    "meta": {
        "doc_date": "2017-05-30",
        "doc_type": "Email",
        "subject": "Re: Snacks at noon with Maxim and his mom?",
        "confidence": "High",
        "processed_by": "ShadowCoder"
    },
    "entities": [
        { "id": "e1", "name": "Lesley Groff", "type": "PERSON" },
        { "id": "e2", "name": "[REDACTED]", "type": "PERSON", "note": "Extracted from blacked-out 'To:' field" },
        { "id": "e3", "name": "Maxim", "type": "PERSON" },
        { "id": "e4", "name": "Maxim's mom", "type": "PERSON", "note": "Implied relative" }
    ],
    "connections": [
        { "from": "e1", "to": "e2", "type": "EMAIL_SENT", "quote": "Sent: Tue 5/30/2017 ... From: Lesley Groff" },
        { "from": "e1", "to": "e3", "type": "MENTIONED", "quote": "appt today with Maxim" },
        { "from": "e1", "to": "e4", "type": "MENTIONED", "quote": "and his mom?" }
    ]
}
```

## 🤖 Supported AI Models

We require high-intelligence models to ensure data accuracy.

*   **Google Gemini 2.0 Flash** (Default)
*   **OpenAI GPT-4o**
*   **Anthropic Claude 3.5 Sonnet**

## 🤝 How to Contribute

We have made it incredibly easy to help. We even have a **Dashboard App** that does the work for you.

👉 **[Read the Contributing Guide](CONTRIBUTING.md)** to download the Dashboard.
👉 **[Join the Community](COMMUNITY.md)** for help.

## 📜 License

This project is open source. Data is meant for public research and transparency.
