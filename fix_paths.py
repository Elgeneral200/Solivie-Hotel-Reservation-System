"""
Quick script to fix all page paths.
Run: python fix_paths.py
"""

import os
import re

def fix_file(filepath):
    """Fix page paths in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all occurrences
    original = content
    content = content.replace('frontend/pages/', 'pages/')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {filepath}")
        return True
    return False

# Fix all Python files
fixed_count = 0

# Fix app.py
if os.path.exists('app.py'):
    if fix_file('app.py'):
        fixed_count += 1

# Fix all pages
if os.path.exists('pages'):
    for filename in os.listdir('pages'):
        if filename.endswith('.py'):
            filepath = os.path.join('pages', filename)
            if fix_file(filepath):
                fixed_count += 1

print(f"\n{'='*60}")
print(f"✅ Fixed {fixed_count} file(s)")
print(f"{'='*60}")
