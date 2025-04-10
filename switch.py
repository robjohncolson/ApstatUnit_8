import json

def read_unit_details(file_path):
    """Read the unit details file and extract placeholder values."""
    placeholders = {}
    pdf_files_array = []
    in_array = False
    array_content = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]  # Don't strip the line here to preserve whitespace
        stripped_line = line.strip()
        
        # Handle simple placeholders
        if ' = %%' in stripped_line and not in_array:
            value, placeholder = stripped_line.split(' = %%', 1)
            placeholder = placeholder.strip('%')
            placeholders[placeholder] = value.strip()
        
        # Start of PDF_FILES_ARRAY
        elif stripped_line.startswith('['):
            in_array = True
            array_content = [line]  # Keep original line with whitespace
            
            # Keep reading until we find the closing bracket followed by = %%PDF_FILES_ARRAY%%
            while i + 1 < len(lines):
                i += 1
                current_line = lines[i]  # Keep original line with whitespace
                stripped_current = current_line.strip()
                array_content.append(current_line)
                
                if stripped_current.endswith('= %%PDF_FILES_ARRAY%%'):
                    # Remove the = %%PDF_FILES_ARRAY%% from the last line but preserve leading whitespace
                    last_line = array_content[-1]
                    leading_space = len(last_line) - len(last_line.lstrip())
                    array_content[-1] = last_line[:leading_space] + stripped_current.split('= %%PDF_FILES_ARRAY%%')[0].rstrip() + '\n'
                    in_array = False
                    break
            
            pdf_files_array = ''.join(array_content)  # Use join without adding extra newlines
        
        i += 1
    
    # Special handling for UNIT_ID
    if 'UNIT_ID' not in placeholders:
        # Try to extract from the content if it exists
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.endswith('=%%UNIT_ID%%'):
                unit_id = stripped_line.split('=')[0].strip()
                placeholders['UNIT_ID'] = unit_id
    
    return placeholders, pdf_files_array

def process_html_template(template_path, output_path, placeholders, pdf_files_array):
    """Process the HTML template and replace placeholders."""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace simple placeholders
    for placeholder, value in placeholders.items():
        content = content.replace(f'%%{placeholder}%%', value)
    
    # Replace PDF_FILES_ARRAY
    if pdf_files_array:
        content = content.replace('%%PDF_FILES_ARRAY%%', pdf_files_array)
    
    # Write the processed content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # File paths
    unit_details_path = 'Unit8SpecificDetails.txt'
    template_path = 'unit9_index_neutral.html'
    output_path = 'unit8_index.html'  # Output will be unit8-specific
    
    try:
        # Read unit details and extract placeholders
        placeholders, pdf_files_array = read_unit_details(unit_details_path)
        
        # Validate that we have all required placeholders
        required_placeholders = ['UNIT_TITLE', 'UNIT_H1', 'UNIT_EXAMWEIGHT', 'UNIT_ID']
        missing = [p for p in required_placeholders if p not in placeholders]
        if missing:
            print(f"Warning: Missing required placeholders: {', '.join(missing)}")
        
        # Process template and create output file
        process_html_template(template_path, output_path, placeholders, pdf_files_array)
        
        print("Successfully processed template!")
        print("\nPlaceholders found and replaced:")
        for k, v in placeholders.items():
            print(f"%%{k}%% -> {v}")
        
        if pdf_files_array:
            print("\nPDF_FILES_ARRAY was processed (multiline JSON)")
            print(f"Length of PDF_FILES_ARRAY: {len(pdf_files_array)} characters")
            
    except Exception as e:
        print(f"Error processing files: {str(e)}")

if __name__ == "__main__":
    main()