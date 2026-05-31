#!/usr/bin/env python3
"""
Validate paper reading JSON against field definitions.
Usage: python validate_paper_json.py -f paper-fields.yaml -j paper_result.json
"""

import argparse, json, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("Error: pyyaml required. pip install pyyaml")
    sys.exit(1)


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_fields(fields_data):
    expected = set()
    for cat_name, fields in fields_data.get('categories', {}).items():
        for field in fields:
            if isinstance(field, dict):
                expected.add(list(field.keys())[0])
    return expected


def validate(fields_data, json_data, json_path):
    expected = extract_fields(fields_data)
    present = set()
    for k, v in json_data.items():
        if k == 'uncertain':
            continue
        if isinstance(v, dict):
            present.update(v.keys())
        else:
            present.add(k)
    missing = [f for f in expected if f not in present]
    has_uncertain = 'uncertain' in json_data

    print(f"\n{'='*60}")
    print(f"Validating: {json_path}")
    print(f"{'='*60}")
    print(f"Expected: {len(expected)} | Present: {len(present)}")
    if missing:
        print(f"\nMISSING ({len(missing)}):")
        for f in sorted(missing):
            print(f"  - {f}")
    else:
        print("\nAll fields present.")
    if has_uncertain:
        u = json_data.get('uncertain', [])
        print(f"Uncertain: {len(u) if isinstance(u, list) else 0}")
        if isinstance(u, list) and u:
            for f in u:
                print(f"  ? {f}")
    else:
        print("WARNING: 'uncertain' array missing")
    print(f"{'='*60}")
    return len(missing) == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fields', required=True)
    parser.add_argument('-j', '--json', required=True)
    args = parser.parse_args()

    if not Path(args.fields).exists():
        print(f"Error: Fields file not found: {args.fields}")
        sys.exit(1)
    if not Path(args.json).exists():
        print(f"Error: JSON file not found: {args.json}")
        sys.exit(1)

    valid = validate(load_yaml(args.fields), load_json(args.json), args.json)
    sys.exit(0 if valid else 1)


if __name__ == '__main__':
    main()
