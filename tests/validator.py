import os
import json

import argparse
import sys
from typing import List, Dict, Any

# We will use simple validation logic here to avoid external dependencies if possible, 
# but for a robust system, 'jsonschema' is recommended.
# For this script, we'll implement the logic described in the design doc.

def validate_structure(data: Dict[str, Any], schema_def: Dict[str, Any]) -> List[str]:
    errors = []
    
    # 1. Syntax is handled by json.load, so if we are here, it is valid JSON.

    # 2. Compliance (Basic checks matching schema.json)
    if "meta" not in data:
        errors.append("Missing 'meta' block")
    else:
        meta = data["meta"]
        required_meta = ["doc_date", "doc_type", "subject", "confidence", "processed_by"]
        for field in required_meta:
            if field not in meta:
                errors.append(f"Missing meta field: {field}")
    
    if "entities" not in data:
        errors.append("Missing 'entities' block")
    
    if "connections" not in data:
        errors.append("Missing 'connections' block")

    return errors

def validate_graph_logic(data: Dict[str, Any]) -> List[str]:
    errors = []
    entity_ids = {e["id"] for e in data.get("entities", [])}
    
    for i, conn in enumerate(data.get("connections", [])):
        if conn["from"] not in entity_ids:
            errors.append(f"Connection {i}: 'from' ID {conn['from']} not found in entities")
        if conn["to"] not in entity_ids:
             errors.append(f"Connection {i}: 'to' ID {conn['to']} not found in entities")
    
    return errors

def validate_file(filepath: str, schema_def: Dict[str, Any]) -> bool:
    print(f"Validating {filepath}...")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  [X] Invalid JSON syntax: {e}")
        return False
    
    structure_errors = validate_structure(data, schema_def)
    if structure_errors:
        print("  [X] Schema Validation Errors:")
        for err in structure_errors:
            print(f"    - {err}")
        return False

    logic_errors = validate_graph_logic(data)
    if logic_errors:
        print("  [X] Graph Logic Errors:")
        for err in logic_errors:
            print(f"    - {err}")
        return False

    print("  [OK] Validation Passed")
    return True

def main():
    parser = argparse.ArgumentParser(description="GitBouncer: Validate contributed JSON files.")
    parser.add_argument("files", nargs='+', help="List of files to validate")
    parser.add_argument("--schema", default="schema.json", help="Path to schema.json")
    
    args = parser.parse_args()
    
    # Load Schema (for reference, though specific validations are hardcoded above for now)
    try:
        with open(args.schema, 'r') as f:
            schema_def = json.load(f)
    except FileNotFoundError:
        print(f"Schema file not found at {args.schema}")
        sys.exit(1)

    all_passed = True
    for filepath in args.files:
        if not validate_file(filepath, schema_def):
            all_passed = False
    
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
