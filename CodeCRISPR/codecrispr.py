
import argparse
import importlib
import os
import sys

LANGUAGE_TOOL_MAP = {
    '.py': 'python_tool',
    '.js': 'javascript_tool',
    '.ts': 'typescript_tool',
    '.php': 'php_tool',
    '.html': 'html_tool',
    '.htm': 'html_tool',
    '.css': 'css_tool',
    '.rs': 'rust_tool',
    '.cpp': 'cpp_tool',
    '.cxx': 'cpp_tool',
    '.cc': 'cpp_tool',
    '.r': 'r_tool',
    '.jl': 'julia_tool',
    '.m': 'matlab_tool',
    '.tex': 'latex_tool',
    '.sps': 'spss_tool',
    '.spss': 'spss_tool'
}

def detect_language(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return LANGUAGE_TOOL_MAP.get(ext)

def load_editor(file_path):
    lang = detect_language(file_path)
    if not lang:
        raise ValueError(f"Unsupported file extension: {file_path}")
    module = importlib.import_module(f'tools.{lang}')
    return module.CodeCRISPR(file_path)

def main():
    parser = argparse.ArgumentParser(description="CodeCRISPR Toolkit")
    parser.add_argument('file', help='Path to the source file')
    parser.add_argument('method', nargs='?', help='Name of the method or block to replace')
    parser.add_argument('code', nargs='?', help='Replacement code (in backticks)')
    parser.add_argument('--inspect', action='store_true', help='Inspect available blocks')
    parser.add_argument('--preview', help='Preview a named block')
    parser.add_argument('--with-lines', action='store_true', help='Include line numbers in preview')
    parser.add_argument('--as-comment', action='store_true', help='Add comment delimiters to each line')
    parser.add_argument('--preview-only', action='store_true', help='Only show the preview, no metadata')
    parser.add_argument('--export', help='Export preview to file')

    args = parser.parse_args()
    editor = load_editor(args.file)

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
            elif not args.preview_only:
                print(f"[PREVIEW] Block '{args.preview}' ({block['start']}–{block['end']})")
                print(preview_text)
            else:
                print(preview_text)
        else:
            print(f"Inspecting '{args.file}' [{detect_language(args.file)}]:")
            for name, pos in editor.reference_map.items():
                print(f"  {name}: lines {pos['start']}–{pos['end']}")
    elif args.method and args.code:
        code = args.code.strip('`')
        editor.replace_method(args.method, code)
        editor.save()
        print(f"[UPDATED] Block '{args.method}' replaced successfully.")
    else:
        print("[ERROR] Invalid usage. Please provide a method name and replacement code, or use --inspect.")
        parser.print_help()

if __name__ == '__main__':
    main()
