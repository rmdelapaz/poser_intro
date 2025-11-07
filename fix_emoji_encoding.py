#!/usr/bin/env python3
"""
Fix Emoji Encoding in HTML Files

This script fixes emoji encoding issues in HTML files, ensuring they display
properly in browsers. It reads files with potential encoding issues and 
re-saves them with proper UTF-8 encoding.

Usage:
    python fix_emoji_encoding.py
    
The script will:
1. Find all lesson_24_firefly_rendering_part_*.html files in the parts directory
2. Read each file and check encoding
3. Re-save with proper UTF-8 encoding
4. Report success/failure for each file
"""

import os
import glob
from pathlib import Path


def fix_emoji_encoding(file_path):
    """
    Fix emoji encoding in a single HTML file.
    
    Args:
        file_path: Path to the HTML file to fix
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Processing: {os.path.basename(file_path)}")
        
        # Try reading with UTF-8 first
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            encoding_used = 'utf-8'
        except UnicodeDecodeError:
            # If UTF-8 fails, try with latin-1
            print(f"  ⚠️ UTF-8 failed, trying latin-1...")
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
            encoding_used = 'latin-1'
        
        # Check if file has proper charset meta tag
        if 'charset="UTF-8"' not in content and 'charset=UTF-8' not in content:
            print(f"  ⚠️ Warning: No UTF-8 charset declaration found!")
        
        # Write back with UTF-8 encoding and Unix line endings
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        print(f"  ✅ Success (read as {encoding_used}, saved as UTF-8)")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False


def main():
    """Main function to process all lesson 24 part files."""
    
    print("=" * 70)
    print("Emoji Encoding Fix Tool for Lesson 24 Parts")
    print("=" * 70)
    print()
    
    # Get the parts directory
    script_dir = Path(__file__).parent
    parts_dir = script_dir / 'parts'
    
    if not parts_dir.exists():
        print(f"❌ Error: Parts directory not found at {parts_dir}")
        return
    
    # Find all lesson 24 part files
    pattern = str(parts_dir / 'lesson_24_firefly_rendering_part_*.html')
    files = sorted(glob.glob(pattern))
    
    if not files:
        print(f"❌ No lesson 24 part files found in {parts_dir}")
        return
    
    print(f"Found {len(files)} files to process:\n")
    
    # Process each file
    success_count = 0
    for file_path in files:
        if fix_emoji_encoding(file_path):
            success_count += 1
        print()
    
    # Summary
    print("=" * 70)
    print(f"Processing Complete: {success_count}/{len(files)} files successful")
    print("=" * 70)
    
    if success_count == len(files):
        print("✅ All files processed successfully!")
        print("\nAll HTML files now have proper UTF-8 encoding for emojis.")
    else:
        print(f"⚠️ {len(files) - success_count} file(s) had errors.")
        print("Please review the errors above.")


if __name__ == '__main__':
    main()
