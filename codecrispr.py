#!/usr/bin/env python3
"""
CodeCRISPR: Precise Code Editing Framework
"""
import argparse
import os
import sys
import importlib.util
import re
import json
import shutil
import difflib
import mimetypes
import configparser
from pathlib import Path

# Extended language mappings with additional file extensions
LANGUAGE_MAP = {
    '.py': 'python_tool',
    '.pyw': 'python_tool',
    '.pyi': 'python_tool',  # Python stub files
    '.js': 'javascript_tool',
    '.mjs': 'javascript_tool',  # ES modules
    '.cjs': 'javascript_tool',  # CommonJS modules
    '.jsx': 'javascript_tool',  # React JSX
    '.ts': 'typescript_tool',
    '.tsx': 'typescript_tool',  # React TSX
    '.html': 'html_tool',
    '.htm': 'html_tool',
    '.css': 'css_tool',
    '.scss': 'css_tool',  # Sass
    '.less': 'css_tool',  # Less
    '.php': 'php_tool',
    '.php3': 'php_tool',
    '.php4': 'php_tool',
    '.php5': 'php_tool',
    '.phtml': 'php_tool',
    '.rs': 'rust_tool',
    '.cpp': 'cpp_tool',
    '.cxx': 'cpp_tool',
    '.cc': 'cpp_tool',
    '.hpp': 'cpp_tool',  # C++ headers
    '.hxx': 'cpp_tool',
    '.h': 'cpp_tool',
    '.r': 'r_tool',
    '.R': 'r_tool',  # R is case-sensitive
    '.m': 'matlab_tool',
    '.tex': 'latex_tool',
    '.sps': 'spss_tool',
    '.spss': 'spss_tool',
    '.md': 'markdown_tool'
}

DEFAULT_CONFIG = {
    'general': {
        'backup_enabled': 'true',
        'backup_extension': '.bak',
        'default_language': 'python_tool',
        'auto_format': 'false'
    },
    'output': {
        'use_colors': 'true',
        'json_pretty': 'true',
        'show_line_numbers': 'false'
    },
    'editor': {
        'tab_size': '4',
        'use_spaces': 'true',
        'trim_trailing_whitespace': 'true'
    }
}

def validate_file_access(filepath):
    """Validate file exists and is readable"""
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    if not os.path.isfile(filepath):
        print(f"[ERROR] Not a file: {filepath}")
        sys.exit(1)
    if not os.access(filepath, os.R_OK):
        print(f"[ERROR] File not readable: {filepath}")
        sys.exit(1)
    return True

def safe_write_file(filepath, content, config=None):
    """Safely write file with backup"""
    if config is None:
        config = load_config()
    
    backup_enabled = config.getboolean('general', 'backup_enabled', fallback=True)
    backup_extension = config.get('general', 'backup_extension', fallback='.bak')
    
    if backup_enabled:
        backup_path = f"{filepath}{backup_extension}"
        try:
            # Create backup if file exists
            if os.path.exists(filepath):
                shutil.copy2(filepath, backup_path)
            
            # Write new content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Remove backup on success
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            return True
        except Exception as e:
            # Restore from backup on failure
            if os.path.exists(backup_path):
                shutil.move(backup_path, filepath)
            print(f"[ERROR] Failed to write file: {e}")
            return False
    else:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to write file: {e}")
            return False

def load_config():
    """Load configuration from ~/.codecrispr/config.ini"""
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)  # Load defaults first
    
    config_dir = os.path.expanduser('~/.codecrispr')
    config_file = os.path.join(config_dir, 'config.ini')
    
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        # Create default config if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
        try:
            with open(config_file, 'w') as f:
                config.write(f)
        except Exception as e:
            print(f"[WARNING] Could not create config file: {e}")
    
    return config

def detect_language(file_path):
    """Enhanced language detection with fallback mechanisms"""
    ext = os.path.splitext(file_path)[1].lower()
    
    # Check our mapping first
    if ext in LANGUAGE_MAP:
        return LANGUAGE_MAP[ext]
    
    # Fallback to mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if 'javascript' in mime_type:
            return 'javascript_tool'
        elif 'python' in mime_type:
            return 'python_tool'
        elif 'php' in mime_type:
            return 'php_tool'
        # Add more mime type mappings as needed
    
    # Check file content for shebang
    try:
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            if first_line.startswith('#!'):
                if 'python' in first_line:
                    return 'python_tool'
                elif 'node' in first_line:
                    return 'javascript_tool'
                elif 'php' in first_line:
                    return 'php_tool'
    except:
        pass
    
    # Load default from config
    config = load_config()
    default_tool = config.get('general', 'default_language', fallback='python_tool')
    print(f"[WARNING] Unknown file type for '{file_path}', defaulting to {default_tool}")
    return default_tool

def load_editor(file_path):
    """Load the appropriate language-specific editor"""
    validate_file_access(file_path)
    tool_name = detect_language(file_path)
    
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tool_path = os.path.join(script_dir, 'tools', f'{tool_name}.py')
        
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        editor = module.CodeCRISPR(file_path)
        return editor
    except Exception as e:
        print(f"[ERROR] Failed to load editor for {tool_name}: {e}")
        sys.exit(1)

def generate_diff(original_lines, new_lines, context_lines=3):
    """Generate a unified diff between original and new content"""
    diff = difflib.unified_diff(
        original_lines,
        new_lines,
        fromfile='original',
        tofile='modified',
        lineterm='',
        n=context_lines
    )
    return '\n'.join(diff)

def show_changes_preview(editor, method_name, new_code):
    """Show a preview of changes before applying them"""
    if method_name not in editor.reference_map:
        print(f"[ERROR] Method '{method_name}' not found.")
        return False
    
    block = editor.reference_map[method_name]
    original_lines = editor.lines[block['start']:block['end'] + 1]
    new_lines = new_code.splitlines()
    
    diff_output = generate_diff(original_lines, new_lines)
    
    print(f"[PREVIEW] Changes to '{method_name}':")
    print(diff_output)
    print("\n[INFO] Use --apply to apply these changes")
    
    return True

def batch_replace_methods(editor, updates):
    """
    Replace multiple methods in a single operation
    updates: list of (method_name, new_code) tuples
    """
    # Sort updates by start position (descending) to avoid offset issues
    sorted_updates = []
    for method_name, new_code in updates:
        if method_name not in editor.reference_map:
            print(f"[WARNING] Method '{method_name}' not found, skipping.")
            continue
        start = editor.reference_map[method_name]['start']
        sorted_updates.append((start, method_name, new_code))
    
    # Sort by start position in descending order
    sorted_updates.sort(reverse=True, key=lambda x: x[0])
    
    # Apply updates from bottom to top to preserve line numbers
    successful_updates = []
    failed_updates = []
    
    for _, method_name, new_code in sorted_updates:
        try:
            editor.replace_method(method_name, new_code)
            successful_updates.append(method_name)
        except Exception as e:
            failed_updates.append((method_name, str(e)))
    
    return successful_updates, failed_updates

def output_as_json(data, config):
    """Output data as JSON for better integration with other tools"""
    pretty = config.getboolean('output', 'json_pretty', fallback=True)
    if pretty:
        return json.dumps(data, indent=2)
    return json.dumps(data)

def main():
    config = load_config()
    
    parser = argparse.ArgumentParser(description="CodeCRISPR: Precise Code Editing Framework")
    parser.add_argument('file', nargs='?', help='Path to the source file')
    parser.add_argument('method', nargs='?', help='Name of the method or block to replace')
    parser.add_argument('code', nargs='?', help='Replacement code (in backticks)')
    
    # Inspection options
    parser.add_argument('--inspect', action='store_true', help='Inspect available blocks')
    parser.add_argument('--preview', help='Preview a named block')
    parser.add_argument('--with-lines', action='store_true', help='Include line numbers in preview')
    parser.add_argument('--as-comment', action='store_true', help='Add comment delimiters to each line')
    parser.add_argument('--preview-only', action='store_true', help='Only show the preview, no metadata')
    parser.add_argument('--export', help='Export preview to file')
    
    # Output formatting
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON output')
    
    # Advanced operations
    parser.add_argument('--batch', help='Batch update from JSON file')
    parser.add_argument('--preview-changes', action='store_true', help='Preview changes before applying')
    parser.add_argument('--apply', action='store_true', help='Apply changes after preview')
    
    # Config options
    parser.add_argument('--config', nargs='?', const='show_all', help='Show or set configuration values (e.g., --config general.backup_enabled=false)')
    
    args = parser.parse_args()
    
    # Handle configuration commands
    if args.config is not None:
        if args.config == 'show_all':
            # Show all configuration
            for section in config.sections():
                print(f"[{section}]")
                for option, value in config.items(section):
                    print(f"  {option} = {value}")
        elif '=' in args.config:
            # Set configuration value
            key, value = args.config.split('=', 1)
            if '.' not in key:
                print(f"[ERROR] Configuration key must be in format: section.option")
                sys.exit(1)
            section, option = key.split('.', 1)
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, option, value)
            config_file = os.path.expanduser('~/.codecrispr/config.ini')
            with open(config_file, 'w') as f:
                config.write(f)
            print(f"[CONFIG] Set {section}.{option} = {value}")
        else:
            # Show configuration value
            if '.' in args.config:
                section, option = args.config.split('.', 1)
                try:
                    value = config.get(section, option)
                    print(f"{section}.{option} = {value}")
                except:
                    print(f"[ERROR] Configuration key not found: {args.config}")
            else:
                print(f"[ERROR] Configuration key must be in format: section.option")
                sys.exit(1)
        return
    
    # Require file argument for non-config operations
    if not args.file:
        parser.error("the following arguments are required: file")
    
    # Load the editor
    try:
        editor = load_editor(args.file)
    except SystemExit:
        return
    
    # Handle batch operations
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                batch_data = json.load(f)
            
            updates = [(item['method'], item['code']) for item in batch_data['updates']]
            successful, failed = batch_replace_methods(editor, updates)
            
            if successful:
                if safe_write_file(args.file, '\n'.join(editor.lines) + '\n', config):
                    print(f"[SUCCESS] Updated {len(successful)} methods: {', '.join(successful)}")
            
            if failed:
                print(f"[WARNING] Failed to update {len(failed)} methods:")
                for method, error in failed:
                    print(f"  - {method}: {error}")
        except Exception as e:
            print(f"[ERROR] Batch update failed: {e}")
        return
    
    # Handle inspection
    if args.inspect:
        if args.preview:
            if args.preview not in editor.reference_map:
                print(f"[ERROR] Block '{args.preview}' not found.")
                return
            
            block = editor.reference_map[args.preview]
            lines = editor.lines[block['start']:block['end'] + 1]
            
            if args.with_lines:
                lines = [f'{i+block["start"]+1}: {line}' for i, line in enumerate(lines)]
            
            if args.as_comment:
                ext = os.path.splitext(args.file)[1]
                comment = '#' if ext in ['.py', '.r', '.jl'] else '//'
                lines = [f'{comment} {line}' for line in lines]
            
            preview_text = '\n'.join(lines)
            
            if args.export:
                with open(args.export, 'w') as f:
                    f.write(preview_text)
                print(f"[SUCCESS] Preview exported to {args.export}")
            elif not args.preview_only:
                print(f"[PREVIEW] Block '{args.preview}' ({block['start']}–{block['end']})")
                print(preview_text)
            else:
                print(preview_text)
        else:
            # Full file inspection
            if args.json:
                result = {
                    'file': args.file,
                    'language': detect_language(args.file),
                    'blocks': {}
                }
                
                for name, pos in editor.reference_map.items():
                    result['blocks'][name] = {
                        'start': pos['start'],
                        'end': pos['end'],
                        'lines': pos['end'] - pos['start'] + 1
                    }
                
                print(output_as_json(result, config))
            else:
                print(f"Inspecting '{args.file}' [{detect_language(args.file)}]:")
                for name, pos in editor.reference_map.items():
                    print(f"  {name}: lines {pos['start']}–{pos['end']}")
    
    # Handle code replacement
    elif args.method and args.code:
        code = args.code.strip('`')
        
        if args.preview_changes and not args.apply:
            show_changes_preview(editor, args.method, code)
        else:
            try:
                editor.replace_method(args.method, code)
                if safe_write_file(args.file, '\n'.join(editor.lines) + '\n', config):
                    print(f"[UPDATED] Block '{args.method}' replaced successfully.")
                else:
                    print(f"[ERROR] Failed to save changes to file.")
            except Exception as e:
                print(f"[ERROR] Failed to replace method: {e}")
    
    else:
        print("[ERROR] Invalid usage. Please provide a method name and replacement code, or use --inspect.")
        parser.print_help()

if __name__ == "__main__":
    main()
