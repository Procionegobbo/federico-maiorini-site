import os
import re

CONTENT_DIR = "content"

# Regex to find image: "something" or image: something
image_pattern = re.compile(r'^(image:\s*)(.+)$', re.MULTILINE)
featured_image_pattern = re.compile(r'^featured_image:\s*.+$', re.MULTILINE)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return

    frontmatter = content[:end_idx]
    body = content[end_idx:]

    if featured_image_pattern.search(frontmatter):
        # Already has featured_image
        return
    
    match = image_pattern.search(frontmatter)
    if match:
        image_val = match.group(2)
        # Use re.sub with count=1 to only replace the FIRST occurrence
        replacement = match.group(0) + f'\nfeatured_image: {image_val}'
        new_frontmatter = re.sub(r'^(image:\s*.*)$', replacement, frontmatter, count=1, flags=re.MULTILINE)
        
        new_content = new_frontmatter + body
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath} with featured_image: {image_val}")

for root, _, files in os.walk(CONTENT_DIR):
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
