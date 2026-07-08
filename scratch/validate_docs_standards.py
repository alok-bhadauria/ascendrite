import os
import re
import sys

def has_emoji(text):
    # Standard emoji ranges in Unicode
    emoji_regex = re.compile(
        r'[\U0001F600-\U0001F64F]'  # emoticons
        r'|[\U0001F300-\U0001F5FF]'  # symbols & pictographs
        r'|[\U0001F680-\U0001F6FF]'  # transport & map
        r'|[\U0001F1E0-\U0001F1FF]'  # flags
        r'|[\u2700-\u27BF]'          # dingbats
        r'|[\u2600-\u26FF]'          # misc symbols
    )
    return bool(emoji_regex.search(text))

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_path = os.path.join(base_dir, "docs")
    editorial_path = os.path.join(base_dir, "editorial")
    
    errors = []
    
    print("Checking markdown files under docs/ and editorial/...")
    
    for path_dir in [docs_path, editorial_path]:
        if not os.path.exists(path_dir):
            continue
            
        for root, dirs, files in os.walk(path_dir):
            for f in files:
                if not f.endswith(".md"):
                    continue
                    
                # 1. Filename kebab-case check
                if not re.match(r'^[a-z0-9-]+.md$', f):
                    errors.append(f"Filename '{f}' is not in kebab-case.md format.")
                    
                file_path = os.path.join(root, f)
                with open(file_path, "r", encoding="utf-8") as file_content:
                    content = file_content.read()
                    
                # 2. Emoji check
                if has_emoji(content):
                    errors.append(f"File '{f}' contains prohibited emojis.")
                    
                # 3. Metadata block check for files in docs/ (except directory-structure.md)
                rel_dir = os.path.relpath(root, base_dir)
                if rel_dir.startswith("docs") and not f == "directory-structure.md":
                    # We check: system-architecture-hld.md, ai-architecture.md, backend-architecture.md,
                    # frontend-architecture.md, database-schema.md, knowledge-base-integration.md, security-standards.md
                    target_files = [
                        "system-architecture-hld.md", "ai-architecture.md", "backend-architecture.md",
                        "frontend-architecture.md", "database-schema.md", "knowledge-base-integration.md",
                        "security-standards.md"
                    ]
                    if f in target_files:
                        if "## Document Metadata" not in content or "*   **Purpose**:" not in content:
                            errors.append(f"File '{f}' is missing standard Metadata Block.")

    if errors:
        print("\nValidation Failed:")
        for err in errors:
            print(f" - {err}")
        return 1
    
    print("\nAll checks passed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
