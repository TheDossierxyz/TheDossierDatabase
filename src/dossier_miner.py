import os
import json
import glob
import time
import argparse
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CONTRIBUTOR_HANDLE = os.getenv("CONTRIBUTOR_HANDLE", "Anonymous")
DEFAULT_MODEL = os.getenv("MODEL_NAME", "gemini-2.0-flash")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schema.json")
INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw_batches")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_schema():
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)

def validate_json(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    required_keys = schema.get("required", [])
    for key in required_keys:
        if key not in data:
            print(f"Validation Error: Missing key '{key}'")
            return False
    return True

def extract_text_from_file(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"Error reading {filepath}. Might be a binary file.")
        return ""

def generate_with_gemini(model_name: str, prompt: str) -> Optional[str]:
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

def generate_with_openai(model_name: str, prompt: str) -> Optional[str]:
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found.")
        return None
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None

def generate_with_anthropic(model_name: str, prompt: str) -> Optional[str]:
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found.")
        return None
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        message = client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Anthropic Error: {e}")
        return None

def process_document(filepath: str, schema: Dict[str, Any], model_name: str):
    filename = os.path.basename(filepath)
    print(f"Processing {filename} with {model_name}...")

    text_content = extract_text_from_file(filepath)
    if not text_content:
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

    # Route to Provider
    json_text = None
    if "gemini" in model_name.lower():
        json_text = generate_with_gemini(model_name, prompt)
    elif "gpt" in model_name.lower():
        json_text = generate_with_openai(model_name, prompt)
    elif "claude" in model_name.lower():
        json_text = generate_with_anthropic(model_name, prompt)
    else:
        print(f"Error: Unknown model provider for {model_name}")
        return

    if not json_text:
        return

    try:
        json_output = json.loads(json_text)
        
        # Inject Metadata
        json_output["meta"]["processed_by"] = CONTRIBUTOR_HANDLE
        json_output["meta"]["model"] = model_name

        # Validate
        if validate_json(json_output, schema):
            output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}.json")
            with open(output_path, 'w') as f:
                json.dump(json_output, f, indent=2)
            print(f"Success: Saved to {output_path}")
        else:
            print(f"Validation Failed for {filename}")

    except json.JSONDecodeError:
        print(f"Error: invalid JSON returned for {filename}")

def main():
    parser = argparse.ArgumentParser(description="Dossier Miner: Extract structured data.")
    parser.add_argument("--batch", help="Batch directory to process", default="")
    parser.add_argument("--model", help="Model to use", default=DEFAULT_MODEL)
    args = parser.parse_args()

    schema = load_schema()
    search_pattern = os.path.join(INPUT_DIR, args.batch, "*.*")
    files = glob.glob(search_pattern)
    
    print(f"Found {len(files)} files. Using model: {args.model}")

    for filepath in files:
        if filepath.lower().endswith(('.txt', '.md', '.pdf')):
            process_document(filepath, schema, args.model)
            time.sleep(1)

if __name__ == "__main__":
    main()
