import os
import json
import glob
import time
import argparse
import mimetypes
from typing import Optional, Dict, Any, Union
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
    """Fallback for text-only models"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        print(f"Error reading {filepath}. Might be a binary file.")
        return ""

def upload_to_gemini(filepath: str, mime_type: str = None):
    """Uploads file to Gemini (for PDF/Image vision)"""
    if not mime_type:
        mime_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    
    print(f"Uploading {filepath} ({mime_type}) to Gemini...")
    file = genai.upload_file(filepath, mime_type=mime_type)
    
    # Wait for processing state to be active
    while file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(1)
        file = genai.get_file(file.name)
    print("Done.")
    return file

def generate_with_gemini(model_name: str, prompt: str, file_path: str = None) -> Optional[str]:
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    
    generation_config = {
        "temperature": 0.0,
        "response_mime_type": "application/json"
    }

    model = genai.GenerativeModel(model_name)
    
    content = [prompt]
    if file_path:
        # Upload the file for vision/multimodal analysis
        gemini_file = upload_to_gemini(file_path)
        content.append(gemini_file)

    try:
        response = model.generate_content(content, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

def generate_with_openai(model_name: str, prompt: str, text_content: str) -> Optional[str]:
    """OpenAI implementation (currently text-only for PDFs)"""
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found.")
        return None
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    full_prompt = f"{prompt}\n\nDOCUMENT TEXT:\n{text_content}"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": full_prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None

def generate_with_anthropic(model_name: str, prompt: str, text_content: str) -> Optional[str]:
    """Anthropic implementation (currently text-only for PDFs)"""
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found.")
        return None
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    full_prompt = f"{prompt}\n\nDOCUMENT TEXT:\n{text_content}"

    try:
        message = client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=[{"role": "user", "content": full_prompt}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Anthropic Error: {e}")
        return None

def process_document(filepath: str, schema: Dict[str, Any], model_name: str):
    filename = os.path.basename(filepath)
    print(f"Processing {filename} with {model_name}...")

    # Load Prompt Template
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt.md")
    try:
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print(f"Error: prompt.md not found at {prompt_path}")
        return

    # Prepare Schema String
    schema_str = json.dumps(schema, indent=2)
    prompt = prompt_template.replace("{{SCHEMA}}", schema_str)

    # Route to Provider
    json_text = None
    
    if "gemini" in model_name.lower():
        # Gemini supports native file upload
        prompt = prompt.replace("{{TEXT}}", "[See Attached File]") 
        json_text = generate_with_gemini(model_name, prompt, filepath)
    else:
        # Other providers (for now) need text extraction
        text_content = extract_text_from_file(filepath)
        if not text_content:
            print("Skipping - content is binary or empty, and model assumes text.")
            return
        # Remove the placeholder from prompt
        prompt = prompt.replace("{{TEXT}}", "") 
        
        if "gpt" in model_name.lower():
            json_text = generate_with_openai(model_name, prompt, text_content)
        elif "claude" in model_name.lower():
            json_text = generate_with_anthropic(model_name, prompt, text_content)
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
        print(json_text)

def main():
    parser = argparse.ArgumentParser(description="Dossier Miner: Extract structured data.")
    parser.add_argument("--batch", help="Batch directory to process", default="")
    parser.add_argument("--model", help="Model to use", default=DEFAULT_MODEL)
    args = parser.parse_args()

    schema = load_schema()
    
    # Supported Extensions (Images + Text + PDF)
    extensions = ('*.txt', '*.md', '*.pdf', '*.jpg', '*.png', '*.jpeg')
    files = []
    
    if args.batch:
        batch_path = os.path.join(INPUT_DIR, args.batch)
        for ext in extensions:
            files.extend(glob.glob(os.path.join(batch_path, ext)))
    else:
        print("Please specify a batch with --batch")
        return
    
    print(f"Found {len(files)} files. Using model: {args.model}")

    for filepath in files:
        process_document(filepath, schema, args.model)
        time.sleep(1)

if __name__ == "__main__":
    main()
