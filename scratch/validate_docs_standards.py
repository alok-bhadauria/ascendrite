import os
import re
import sys

def has_emoji(text):
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
    blueprint_path = os.path.join(base_dir, "blueprint")
    
    errors = []
    seen_filenames = {}
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]*)\)')
    
    print("Executing comprehensive documentation QA validations...")
    
    # 1. Gather all files and check naming, duplicate filenames, metadata structures, and emojis
    for path_dir in [docs_path, editorial_path, blueprint_path]:
        if not os.path.exists(path_dir):
            continue
            
        for root, dirs, files in os.walk(path_dir):
            for f in files:
                if not f.endswith(".md"):
                    continue
                
                rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                
                # Check duplicate filenames (excluding README.md which can exist per directory)
                if f.lower() != "readme.md":
                    if f in seen_filenames:
                        errors.append(f"Duplicate filename detected: '{f}' in '{rel_path}' and '{seen_filenames[f]}'")
                    else:
                        seen_filenames[f] = rel_path
                
                # Check naming convention
                if f.lower() != "readme.md" and not re.match(r'^[a-z0-9-]+.md$', f):
                    errors.append(f"Filename '{f}' in '{rel_path}' is not in kebab-case.md format.")
                    
                file_path = os.path.join(root, f)
                with open(file_path, "r", encoding="utf-8") as file_content:
                    content = file_content.read()
                    
                # Check for prohibited emojis
                if has_emoji(content):
                    errors.append(f"File '{rel_path}' contains prohibited Unicode emojis.")
                    
                # Check standard Metadata Block
                rel_dir = os.path.relpath(root, base_dir)
                if rel_dir.startswith("docs") and not f == "directory-structure.md":
                    target_files = [
                        "system-architecture-hld.md", "ai-architecture.md", "backend-architecture.md",
                        "frontend-architecture.md", "database-schema.md", "knowledge-base-integration.md",
                        "security-standards.md", "project-vision.md", "product-philosophy.md",
                        "learning-philosophy.md", "engineering-principles.md", "platform-philosophy.md",
                        "ai-philosophy.md", "organizational-structure.md", "product-evolution-strategy.md",
                        "version-roadmap.md", "engineering-decision-process.md"
                    ]
                    if f in target_files:
                        if "## Document Metadata" not in content or "*   **Purpose**:" not in content or "*   **Scope**:" not in content or "*   **Ownership**:" not in content:
                            errors.append(f"File '{rel_path}' is missing the standardized Metadata Block (Purpose, Scope, Audience, Ownership, Related Documents).")
 
                # 2. Link verification check
                matches = link_pattern.findall(content)
                for text, link in matches:
                    # Fail on local absolute file links
                    if link.startswith("file:"):
                        errors.append(f"Absolute local file link detected in '{rel_path}': '{link}'")
                        continue
                        
                    if link.startswith("http") or link.startswith("mailto:") or link.startswith("#"):
                        continue
                        
                    clean_link = link.split("#")[0].split("?")[0]
                    if not clean_link:
                        continue
                        
                    target_path = os.path.normpath(os.path.join(root, clean_link))
                    if not os.path.exists(target_path):
                        errors.append(f"Broken link in '{rel_path}': target path not found for '{link}'")
 
    if errors:
        print("\nDocumentation Validation Checks Failed:")
        for err in errors:
            print(f" - {err}")
        return 1
    
    print("\nAll documentation standards and reference links verified successfully!")
    return 0
 
if __name__ == "__main__":
    sys.exit(main())
