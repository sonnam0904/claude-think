#!/usr/bin/env python3
"""Validation script for Dify plugin precheck workflow."""

import os
import sys
import yaml
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> tuple[bool, str]:
    """Check if a file exists."""
    if os.path.exists(filepath):
        return True, f"✅ {description}: {filepath}"
    return False, f"❌ {description} NOT FOUND: {filepath}"

def check_manifest() -> list[tuple[bool, str]]:
    """Check manifest.yaml requirements."""
    results = []
    manifest_path = "manifest.yaml"
    
    if not os.path.exists(manifest_path):
        results.append((False, "❌ manifest.yaml NOT FOUND"))
        return results
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
        
        # Check author
        author = manifest.get('author', '')
        if author in ['langgenius', 'dify']:
            results.append((False, f"❌ Author cannot be '{author}' (must not be 'langgenius' or 'dify')"))
        else:
            results.append((True, f"✅ Author is valid: {author}"))
        
        # Check required fields
        required_fields = ['version', 'author', 'name', 'type']
        for field in required_fields:
            if field in manifest:
                results.append((True, f"✅ Required field '{field}' present: {manifest[field]}"))
            else:
                results.append((False, f"❌ Required field '{field}' missing"))
        
        # Check Python version
        python_version = manifest.get('meta', {}).get('runner', {}).get('version', '')
        if python_version == '3.12':
            results.append((True, f"✅ Python version is 3.12: {python_version}"))
        else:
            results.append((False, f"⚠️  Python version is {python_version}, should be 3.12"))
        
    except Exception as e:
        results.append((False, f"❌ Error reading manifest.yaml: {e}"))
    
    return results

def check_icon() -> list[tuple[bool, str]]:
    """Check icon requirements."""
    results = []
    
    # Read manifest to get icon filename
    try:
        with open("manifest.yaml", 'r') as f:
            manifest = yaml.safe_load(f)
        icon_filename = manifest.get('icon', 'icon.svg')
    except:
        icon_filename = 'icon.svg'
    
    icon_path = f"_assets/{icon_filename}"
    
    # Check if icon exists
    exists, msg = check_file_exists(icon_path, "Icon file")
    results.append((exists, msg))
    
    if exists:
        # Check for placeholder text
        try:
            with open(icon_path, 'r') as f:
                icon_content = f.read()
            
            if 'DIFY_MARKETPLACE_TEMPLATE_ICON_DO_NOT_USE' in icon_content:
                results.append((False, "❌ Icon contains placeholder text 'DIFY_MARKETPLACE_TEMPLATE_ICON_DO_NOT_USE'"))
            else:
                results.append((True, "✅ Icon does not contain placeholder text"))
            
            # Check if it's default template (simplified check)
            default_patterns = [
                '<path d="M20 20 V80 M20 20 H60 Q80 20 80 40 T60 60 H20"',
                'fill="none"',
                'stroke="black"',
                'stroke-width="5"'
            ]
            if all(pattern in icon_content for pattern in default_patterns):
                results.append((False, "⚠️  Icon might be default template (contains default SVG patterns)"))
            else:
                results.append((True, "✅ Icon appears to be customized"))
                
        except Exception as e:
            results.append((False, f"❌ Error reading icon file: {e}"))
    
    return results

def check_required_files() -> list[tuple[bool, str]]:
    """Check all required files exist."""
    results = []
    
    required_files = [
        ("manifest.yaml", "Manifest file"),
        ("README.md", "README file"),
        ("PRIVACY.md", "Privacy policy"),
        ("requirements.txt", "Dependencies file"),
        ("provider/think_provider.yaml", "Provider YAML"),
        ("provider/think_provider.py", "Provider Python"),
        ("tools/think.yaml", "Tool YAML"),
        ("tools/think_tool.py", "Tool Python"),
        ("main.py", "Entry point"),
    ]
    
    for filepath, description in required_files:
        exists, msg = check_file_exists(filepath, description)
        results.append((exists, msg))
    
    return results

def check_requirements_txt() -> list[tuple[bool, str]]:
    """Check requirements.txt can be parsed."""
    results = []
    
    if not os.path.exists("requirements.txt"):
        results.append((False, "❌ requirements.txt not found"))
        return results
    
    try:
        with open("requirements.txt", 'r') as f:
            lines = f.readlines()
        
        if len(lines) > 0:
            results.append((True, f"✅ requirements.txt has {len(lines)} lines"))
            
            # Check for dify-plugin
            content = ''.join(lines)
            if 'dify-plugin' in content:
                results.append((True, "✅ requirements.txt contains dify-plugin"))
            else:
                results.append((False, "⚠️  requirements.txt does not contain dify-plugin"))
        else:
            results.append((False, "❌ requirements.txt is empty"))
            
    except Exception as e:
        results.append((False, f"❌ Error reading requirements.txt: {e}"))
    
    return results

def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Dify Plugin Precheck Validation")
    print("=" * 60)
    print()
    
    all_passed = True
    all_results = []
    
    # Check manifest
    print("📋 Checking manifest.yaml...")
    manifest_results = check_manifest()
    all_results.extend(manifest_results)
    for passed, msg in manifest_results:
        print(f"  {msg}")
        if not passed:
            all_passed = False
    print()
    
    # Check icon
    print("🖼️  Checking icon...")
    icon_results = check_icon()
    all_results.extend(icon_results)
    for passed, msg in icon_results:
        print(f"  {msg}")
        if not passed:
            all_passed = False
    print()
    
    # Check required files
    print("📁 Checking required files...")
    file_results = check_required_files()
    all_results.extend(file_results)
    for passed, msg in file_results:
        print(f"  {msg}")
        if not passed:
            all_passed = False
    print()
    
    # Check requirements.txt
    print("📦 Checking requirements.txt...")
    req_results = check_requirements_txt()
    all_results.extend(req_results)
    for passed, msg in req_results:
        print(f"  {msg}")
        if not passed:
            all_passed = False
    print()
    
    # Summary
    print("=" * 60)
    total_checks = len(all_results)
    passed_checks = sum(1 for passed, _ in all_results if passed)
    
    print(f"Summary: {passed_checks}/{total_checks} checks passed")
    print()
    
    if all_passed:
        print("✅ All checks PASSED! Plugin is ready for precheck workflow.")
        return 0
    else:
        print("⚠️  Some checks FAILED. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
