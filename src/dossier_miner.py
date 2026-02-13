import os
import json
import glob
import time
import argparse
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
# import openai  # Uncomment if supporting OpenAI

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
CONTRIBUTOR_HANDLE = os.getenv("CONTRIBUTOR_HANDLE", "Anonymous")
MODEL_NAME = "gemini-1.5-flash"  # Creating a default, can be overridden
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schema.json")
INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw_batches")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_schema():
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)

def validate_json(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    # This is a basic validation. For strict validation, use the jsonschema library.
    # In a real scenario, we'd use the 'jsonschema' pip package.
    # For now, we'll check key structural elements.
    required_keys = schema.get("required", [])
    for key in required_keys:
        if key not in data:
            print(f"Validation Error: Missing key '{key}'")
            return False
    return True

def extract_text_from_file(filepath: str) -> str:
    # Placeholder for text extraction logic
    # In a real implementation, this would use pypdf or similar for PDFs
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"Error reading {filepath}. Might be a binary file.")
        return ""

def process_document(filepath: str, schema: Dict[str, Any]):
    filename = os.path.basename(filepath)
    print(f"Processing {filename}...")

    text_content = extract_text_from_file(filepath)
    if not text_content:
        print(f"Skipping {filename} due to empty content.")
        return

    # Load Prompt Template
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt.md")
    try:
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print(f"Error: prompt.md not found at {prompt_path}")
        return

    # Construct Prompt
    prompt = prompt_template.replace("{{SCHEMA}}", json.dumps(schema, indent=2)).replace("{{TEXT}}", text_content)

    try:
        # Call Gemini API
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        
        try:
            json_output = json.loads(response.text)
        except json.JSONDecodeError:
            print(f"Error: LLM did not return valid JSON for {filename}")
            return

        # Inject Metadata
        json_output["meta"]["processed_by"] = CONTRIBUTOR_HANDLE
        # json_output["meta"]["source_file"] = filename # Optional, good for tracking

        # Validate
        if validate_json(json_output, schema):
            output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}.json")
            with open(output_path, 'w') as f:
                json.dump(json_output, f, indent=2)
            print(f"Success: Saved to {output_path}")
        else:
            print(f"Validation Failed for {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Dossier Miner: Extract structured data from documents.")
    parser.add_argument("--batch", help="Specific batch directory to process", default="")
    args = parser.parse_args()

    schema = load_schema()

    # Search for files
    search_pattern = os.path.join(INPUT_DIR, args.batch, "*.*")
    files = glob.glob(search_pattern)
    
    print(f"Found {len(files)} files to process.")

    for filepath in files:
        if filepath.lower().endswith(('.txt', '.md', '.pdf')): # Add other extensions as needed
            process_document(filepath, schema)
            time.sleep(1) # Basic rate limiting

if __name__ == "__main__":
    main()
