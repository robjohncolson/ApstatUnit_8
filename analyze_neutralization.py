import re
from pathlib import Path

def identify_unit_specific_content(file_path):
    """Identify unit-specific content that needs to be neutralized."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find unit-specific content patterns
    unit_specific = {
        'title': re.search(r'<title>.*?</title>', content, re.DOTALL),
        'header': re.search(r'<h1.*?>.*?</h1>', content, re.DOTALL),
        'exam_weight': re.search(r'Exam Weight:.*?</div>', content, re.DOTALL),
        'unit_id': re.search(r"const\s+UNIT_ID\s*=\s*'[0-9]'", content),
        'pdf_files': re.search(r'const\s+pdfFiles\s*=\s*\[.*?\];', content, re.DOTALL),
    }
    
    # Extract the actual content that needs to be neutralized
    neutralization_targets = {}
    for key, match in unit_specific.items():
        if match:
            neutralization_targets[key] = match.group(0)
    
    return neutralization_targets

def generate_neutralization_guide(file_path):
    """Generate a guide for neutralizing unit-specific content."""
    targets = identify_unit_specific_content(file_path)
    
    print("\nNeutralization Guide for Unit 9:")
    print("\nThe following unit-specific content needs to be replaced with placeholders:")
    
    for key, content in targets.items():
        print(f"\n{key.upper()}:")
        print(f"Current content: {content}")
        print(f"Replace with: {get_placeholder(key)}")

def get_placeholder(key):
    """Get the appropriate placeholder for a given key."""
    placeholders = {
        'title': '%%UNIT_TITLE%%',
        'header': '%%UNIT_H1%%',
        'exam_weight': '%%UNIT_EXAMWEIGHT%%',
        'unit_id': '%%UNIT_ID%%',
        'pdf_files': '%%PDF_FILES_ARRAY%%'
    }
    return placeholders.get(key, f'%%{key.upper()}%%')

def main():
    # Path to the current Unit 9 file
    unit9_path = 'unit9-index-loaded.html'  # Using the loaded version as it has the current state
    
    # Generate neutralization guide
    generate_neutralization_guide(unit9_path)

if __name__ == "__main__":
    main() 