import os
import json
import re
import sys

# Ensure UTF-8 output encoding for standard streams
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def check_for_emoji(text):
    for char in text:
        cp = ord(char)
        # Check standard emoji ranges:
        # Miscellaneous Symbols and Pictographs: 1F300-1F5FF
        # Emoticons: 1F600-1F64F
        # Transport and Map Symbols: 1F680-1F6FF
        # Supplemental Symbols and Pictographs: 1F900-1F9FF
        # Symbols and Pictographs Extended-A: 1FA70-1FAFF
        # Dingbats: 2700-27BF
        # Miscellaneous Symbols: 2600-26FF
        if (0x1F300 <= cp <= 0x1FAFF) or (0x2600 <= cp <= 0x27BF):
            return True
    return False

def check_for_absolute_paths(text):
    # Clean up standard escape sequences to avoid matching variable names in print statements (e.g. X:\n)
    text_clean = text.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
    # Match Windows drive paths (e.g., C:\...) or file:/// protocols or Unix absolute paths
    path_pattern = re.compile(r'(?:\b[a-zA-Z]:\\|\b[a-zA-Z]:/|file:///|/home/|/Users/)')
    return bool(path_pattern.search(text_clean))

def validate_subject(subject_path):
    subject_id = os.path.basename(subject_path)
    print(f"Validating subject: {subject_id}")
    errors = []

    # 1. Check metadata files exist
    required_files = [
        "syllabus.json",
        "subject-metadata.json",
        "knowledge-assets.json",
        "book-metadata.json",
        "subject-map.json"
    ]
    for filename in required_files:
        filepath = os.path.join(subject_path, filename)
        if not os.path.exists(filepath):
            errors.append(f"Missing required file: {filename}")
            continue
        
    def check_json_object_for_errors(data):
        if isinstance(data, dict):
            for k, v in data.items():
                err = check_json_object_for_errors(k) or check_json_object_for_errors(v)
                if err:
                    return err
        elif isinstance(data, list):
            for item in data:
                err = check_json_object_for_errors(item)
                if err:
                    return err
        elif isinstance(data, str):
            if check_for_emoji(data):
                return "emoji"
            if check_for_absolute_paths(data):
                return "absolute_path"
        return None

    for filename in required_files:
        filepath = os.path.join(subject_path, filename)
        if not os.path.exists(filepath):
            errors.append(f"Missing required file: {filename}")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                err = check_json_object_for_errors(data)
                if err == "emoji":
                    errors.append(f"Emoji detected in {filename}")
                elif err == "absolute_path":
                    errors.append(f"Absolute path reference detected in {filename}")
        except json.JSONDecodeError as e:
            errors.append(f"JSON decode error in {filename}: {e}")
        except Exception as e:
            errors.append(f"Error reading {filename}: {e}")

    # 2. Check all subdirectories for valid JSON files
    subdirs = ["notes", "quiz", "practice", "examples", "revision", "interview", "diagrams"]
    for subdir in subdirs:
        subdir_path = os.path.join(subject_path, subdir)
        if os.path.exists(subdir_path):
            for file in os.listdir(subdir_path):
                if file.endswith(".json"):
                    filepath = os.path.join(subdir_path, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            err = check_json_object_for_errors(data)
                            if err == "emoji":
                                errors.append(f"Emoji detected in {subdir}/{file}")
                            elif err == "absolute_path":
                                errors.append(f"Absolute path reference detected in {subdir}/{file}")
                    except json.JSONDecodeError as e:
                        errors.append(f"JSON decode error in {subdir}/{file}: {e}")
                    except Exception as e:
                        errors.append(f"Error reading {subdir}/{file}: {e}")
                elif file.endswith((".py", ".md")):
                    errors.append(f"Unconverted file format remaining: {subdir}/{file}")

    return errors

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    all_errors = {}
    
    for category in ["ai", "core-cs", "software-engineering", "web-development", "aptitude"]:
        kb_path = os.path.join(base_dir, "knowledge-base", category)
        if not os.path.exists(kb_path):
            continue
            
        for subject in os.listdir(kb_path):
            subject_path = os.path.join(kb_path, subject)
            if os.path.isdir(subject_path):
                errors = validate_subject(subject_path)
                if errors:
                    all_errors[f"{category}/{subject}"] = errors

    if all_errors:
        print("\nValidation Failed!")
        for subject, errors in all_errors.items():
            print(f"\nSubject '{subject}' has the following errors:")
            for err in errors:
                try:
                    print(f" - {err}")
                except Exception:
                    # Fallback for console encoding issues if print still fails
                    print(f" - {err.encode('ascii', errors='replace').decode('ascii')}")
        sys.exit(1)
    else:
        print("\nAll subjects validated successfully with no errors!")
        sys.exit(0)

if __name__ == "__main__":
    main()
