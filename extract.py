import re
from bs4 import BeautifulSoup

def extract_and_save_details(soup, output_file):
    """Extract unit details and save them to a file"""
    # Extract UNIT_TITLE
    title = soup.find('title').string.strip()
    
    # Extract UNIT_H1
    h1 = soup.find('h1', class_='text-3xl').string.strip()
    
    # Extract UNIT_EXAMWEIGHT
    exam_weight_div = soup.find('div', class_='bg-yellow-100')
    exam_weight = exam_weight_div.find('span', class_='font-semibold').next_sibling.strip()
    
    # Extract UNIT_ID from script
    scripts = soup.find_all('script')
    unit_id = None
    for script in scripts:
        if script.string and 'UNIT_ID' in script.string:
            match = re.search(r"const UNIT_ID = '(\d+)'", script.string)
            if match:
                unit_id = match.group(1)
                break
    
    # Extract PDF_FILES_ARRAY from script
    pdf_files_array = None
    for script in scripts:
        if script.string and 'pdfFiles = [' in script.string:
            start_idx = script.string.find('pdfFiles = [')
            end_idx = script.string.find('];', start_idx) + 1
            if start_idx >= 0 and end_idx > start_idx:
                pdf_files_array = script.string[start_idx + len('pdfFiles = '):end_idx].strip()
    
    # Write extracted details to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{title} = %%UNIT_TITLE%%\n")
        f.write(f"{h1} = %%UNIT_H1%%\n")
        f.write(f"{exam_weight} = %%UNIT_EXAMWEIGHT%%\n")
        if unit_id:
            f.write(f"{unit_id}=%%UNIT_ID%%\n")
        if pdf_files_array:
            f.write(f"{pdf_files_array} = %%PDF_FILES_ARRAY%%\n")

def format_html(input_file, output_file, details_file):
    # Read the input HTML file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse HTML with BeautifulSoup while preserving whitespace
    soup = BeautifulSoup(content, 'html.parser')

    # Extract details before making replacements
    extract_and_save_details(soup, details_file)

    # Fix specific formatting issues
    
    # 1. Fix head section spacing and structure
    head = soup.find('head')
    if head:
        # Ensure proper meta tag order and formatting
        meta_charset = soup.find('meta', attrs={'charset': True})
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        if meta_charset and meta_viewport:
            meta_charset['charset'] = 'UTF-8'  # Standardize charset casing
            meta_viewport['content'] = 'width=device-width, initial-scale=1.0'
            # Ensure proper order: charset, viewport, title
            if meta_charset.next_sibling != meta_viewport:
                meta_charset.insert_after(meta_viewport)

        # Add newlines between head elements with 4-space indentation
        for tag in head.find_all(recursive=False):
            tag.insert_before('\n    ')
            # Add extra newline before script sections
            if tag.name == 'script' and tag.previous_sibling and tag.previous_sibling.name != 'script':
                tag.insert_before('\n')
        head.append('\n')

    # 2. Fix script tags formatting
    for script in soup.find_all('script'):
        # Keep script tags on one line if they're empty or just have src attribute
        if not script.string and not script.contents:
            script.string = ''
            script.append('\n')  # Ensure proper closing
        # Remove extra whitespace in script attributes
        if script.get('src'):
            script['src'] = script['src'].strip()

    # 3. Fix specific placeholders and content
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = '%%UNIT_TITLE%%'

    h1_tag = soup.find('h1', class_='text-3xl')
    if h1_tag:
        h1_tag.string = '%%UNIT_H1%%'
        # Ensure proper closing tag
        h1_tag.name = 'h1'  # This ensures proper tag closure

    # Fix exam weight section
    exam_weight_div = soup.find('div', class_='bg-yellow-100')
    if exam_weight_div:
        exam_weight_span = exam_weight_div.find('span', class_='font-semibold')
        if exam_weight_span:
            exam_weight_span.string = 'Exam Weight:'
            # Create or update the exam weight placeholder
            next_span = exam_weight_span.find_next_sibling('span')
            if not next_span:
                next_span = soup.new_tag('span')
                exam_weight_span.insert_after(next_span)
            next_span.string = ' %%UNIT_EXAMWEIGHT%%'

    # 4. Fix body section formatting
    body = soup.find('body')
    if body:
        # Ensure proper container div spacing
        container = body.find('div', class_='container')
        if container:
            container.insert_before('\n    ')
            container.append('\n')

    # 5. Format the output with proper indentation and spacing
    formatted_html = str(soup.prettify())
    
    # 6. Fix specific formatting preferences
    # Fix empty script tags
    formatted_html = re.sub(r'<script([^>]*)>\s*</script>', r'<script\1></script>', formatted_html)
    # Fix self-closing tags
    formatted_html = re.sub(r'<link([^>]*)>\s*</link>', r'<link\1>', formatted_html)
    # Fix extra newlines between scripts
    formatted_html = re.sub(r'(\n\s*\n\s*)<script', r'\n    <script', formatted_html)
    # Fix comment spacing
    formatted_html = re.sub(r'<!--\s+', '<!-- ', formatted_html)
    formatted_html = re.sub(r'\s+-->', ' -->', formatted_html)
    # Fix placeholder spacing
    formatted_html = re.sub(r'%%\s+', '%%', formatted_html)
    formatted_html = re.sub(r'\s+%%', '%%', formatted_html)

    # Write the formatted HTML to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_html)

# Run the formatter
format_html('unit8_index_loaded.html', 'unit8_index_neutral.html', 'ExtractedUnit8Details.txt')