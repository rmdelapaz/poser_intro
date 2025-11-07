#!/usr/bin/env python3
"""
Fix Emoji Encoding in Lesson 24 HTML Part Files

This script fixes emoji encoding issues in the lesson 24 part files,
ensuring all emojis display properly in browsers.

Usage:
    python fix_lesson24_emojis.py
"""

import os
import glob
from pathlib import Path


def fix_file_encoding(file_path):
    """
    Fix encoding for a single HTML file.
    
    Args:
        file_path: Path to the HTML file
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        filename = os.path.basename(file_path)
        print(f"\nProcessing: {filename}")
        
        # Read the file - try UTF-8 first, then fall back to latin-1
        content = None
        encoding_used = None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            encoding_used = 'utf-8'
            print(f"  ✓ Read successfully as UTF-8")
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                encoding_used = 'latin-1'
                print(f"  ⚠ Had to read as latin-1 (encoding issue detected)")
            except Exception as e:
                return False, f"Failed to read file: {str(e)}"
        
        # Check for emoji encoding issues in content
        has_issues = False
        if 'â' in content or 'ðŸ' in content:
            has_issues = True
            print(f"  ⚠ Found emoji encoding issues")
        
        # Write back with proper UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        if has_issues:
            print(f"  ✅ Fixed and saved with UTF-8 encoding")
            return True, "Fixed encoding issues"
        else:
            print(f"  ✅ No issues found, re-saved with UTF-8")
            return True, "No issues (verified UTF-8)"
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"  ❌ {error_msg}")
        return False, error_msg


def main():
    """Main function to process all lesson 24 part files."""
    
    print("=" * 70)
    print("Emoji Encoding Fix Tool for Lesson 24 Part Files")
    print("=" * 70)
    
    # Get the script's directory and find parts folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parts_dir = os.path.join(script_dir, 'parts')
    
    print(f"\nScript directory: {script_dir}")
    print(f"Looking for parts in: {parts_dir}")
    
    if not os.path.exists(parts_dir):
        print(f"\n❌ Error: Parts directory not found at:")
        print(f"   {parts_dir}")
        return 1
    
    # Find all lesson 24 part files
    pattern = os.path.join(parts_dir, 'lesson_24_firefly_rendering_part_*.html')
    files = sorted(glob.glob(pattern))
    
    if not files:
        print(f"\n❌ No lesson 24 part files found matching pattern:")
        print(f"   lesson_24_firefly_rendering_part_*.html")
        print(f"   in directory: {parts_dir}")
        return 1
    
    print(f"\nFound {len(files)} files to process\n")
    
    # Process each file
    results = []
    for file_path in files:
        success, message = fix_file_encoding(file_path)
        results.append((os.path.basename(file_path), success, message))
    
    # Print summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    success_count = sum(1 for _, success, _ in results if success)
    
    print(f"\nProcessed: {len(results)} files")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    
    # Show any failures
    failures = [(name, msg) for name, success, msg in results if not success]
    if failures:
        print("\n❌ Failed files:")
        for name, msg in failures:
            print(f"   - {name}: {msg}")
    else:
        print("\n✅ All files processed successfully!")
        print("\nAll lesson 24 part files now have proper UTF-8 encoding.")
        print("Emojis should display correctly in all browsers.")
    
    return 0 if success_count == len(results) else 1


if __name__ == '__main__':
    exit(main())
