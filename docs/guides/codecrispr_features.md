# CodeCRISPR Features Overview

This document provides a comprehensive summary of **all features currently supported by CodeCRISPR**, with an emphasis on how they may be used by either a human user or an AI agent via the MCP interface.

---

## Core Capabilities

### Reference Mapping
- CodeCRISPR builds a reference map that identifies the **location of functions, methods, blocks, or sections** in supported file types.
- The map is used to quickly locate, replace, or preview a named code block.
- This reference map is specific to the language of the file and is updated after each modification.

### Block Replacement
- Users or AI can issue a request to **replace a named function or block** with new content.
- CodeCRISPR performs a structural replacement without modifying unrelated parts of the file.
- Replacements update the reference map in-memory without requiring a re-parse of the entire file.

### Diff Output
- Each replacement operation can generate a **Git-style unified diff** that highlights:
  - Removed lines (`-`)
  - Added lines (`+`)
  - Context lines (unchanged)
- Using the `--preview-changes` flag, users can see the impact of changes before applying them.
- Diffs include:
  - Original and modified file labels
  - A "hunk" header showing line numbers and method name
  - Line-level changes with context (3 lines by default)

### Section Preview
- Users or AI agents can request to preview the **current contents of any named method or section** before deciding whether to modify it.
- This preview uses the reference map to extract only the relevant lines from the file.
- The command `--inspect --preview "method_name"` displays the code for that block only.

---

## Command Line Options

CodeCRISPR provides a comprehensive set of command line flags:

### Basic Operations
- `file`, `method`, `code`: Basic positional arguments for specifying the target file, method to replace, and new code
- `--inspect`: Inspect available blocks in a file
- `--preview [method_name]`: Preview a specific named block

### Preview Customization
- `--with-lines`: Include line numbers in preview
- `--as-comment`: Add comment delimiters to each line of the preview
- `--preview-only`: Show only the preview content, no metadata
- `--export [file]`: Export preview to specified file

### Output Formatting
- `--json`: Output in JSON format for better integrations
- `--pretty`: Pretty print JSON output

### Advanced Operations
- `--batch [json_file]`: Batch update from JSON file
- `--preview-changes`: Preview changes before applying them
- `--apply`: Apply changes after preview

### Configuration
- `--config`: Show or set configuration values (e.g., `--config general.backup_enabled=false`)

---

## Performance Characteristics

- **Initial parse** is O(n) where n is the number of lines.
- **Subsequent operations** (e.g., replacement, preview) are constant time (O(1)) thanks to the reference map.
- **Edits are performed in memory**, with disk writes only when explicitly saved.
- **Incremental map updates** allow efficient management of large files, up to tens of thousands of lines.

---

## File Types and Parsers

Each supported file type has a dedicated parsing strategy, defined in the `LANGUAGE_MAP` dictionary:

- Python (`.py`, `.pyw`, `.pyi`): Indentation-based
- JavaScript/TypeScript (`.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.tsx`): Pattern-based
- HTML (`.html`, `.htm`): Tag-based
- CSS (`.css`, `.scss`, `.less`): Block-based
- PHP (`.php`, `.php3`, `.php4`, `.php5`, `.phtml`): Pattern-based
- Rust (`.rs`): Pattern-based
- C++ (`.cpp`, `.cxx`, `.cc`, `.hpp`, `.hxx`, `.h`): Pattern-based
- R (`.r`, `.R`): Pattern-based
- MATLAB (`.m`): Pattern-based
- LaTeX (`.tex`): Environment-based
- SPSS (`.sps`, `.spss`): Block-based
- Markdown (`.md`): Heading-based

The system is designed to be extensible with additional language parsers.

---

## Configuration System

CodeCRISPR includes a configurable settings system:

### General Settings
- `backup_enabled`: Whether to create backup files (default: true)
- `backup_extension`: Extension for backup files (default: '.bak')
- `default_language`: Default language tool to use for unknown file types
- `auto_format`: Whether to auto-format code (default: false)

### Output Settings
- `use_colors`: Whether to use colors in output (default: true)
- `json_pretty`: Whether to pretty-print JSON output (default: true)
- `show_line_numbers`: Whether to show line numbers (default: false)

### Editor Settings
- `tab_size`: Tab size for editing (default: 4)
- `use_spaces`: Whether to use spaces instead of tabs (default: true)
- `trim_trailing_whitespace`: Whether to trim trailing whitespace (default: true)

Settings are stored in `~/.codecrispr/config.ini` and can be modified via the `--config` flag.

---

## Backup System

- If `backup_enabled = true`, CodeCRISPR creates `.bak` files before modification.
- The `backup_extension` config option allows customization of the backup file extension.
- This ensures recovery is always possible even if an operation fails.
- When operations succeed, backup files are automatically removed.

---

## Token Efficiency

- CodeCRISPR minimizes token usage by operating only on relevant sections.
- It avoids full-file reads/writes unless explicitly instructed.
- This results in 80–90% token savings in typical multi-edit workflows compared to naive AI editing.

---

## AI Integration Features

CodeCRISPR was designed with **AI-agent workflows** in mind:

- **Zero installation**: Runs with native Python on macOS (no extra packages required).
- **CLI-driven**: Accepts clean command-line invocations like `python3 codecrispr.py file.py "method" "new_code"`.
- **Inspectable interface**: AI can request the list of functions (`--inspect`) and preview specific ones.
- **Safe retry behavior**: If a change fails due to name mismatch, no file is altered.
- **Error messages**: Human-readable and designed for easy parsing by AI (e.g., `Function 'foo' not found`).

---

## Batch Operations

- CodeCRISPR supports JSON-based batch editing with the `--batch` flag:
```json
{
  "updates": [
    { "method": "foo", "code": "..." },
    { "method": "bar", "code": "..." }
  ]
}
```
- This allows AI or users to edit many parts of a file efficiently in one invocation.
- Batch operations are applied in descending order of start line to avoid offset issues.
- Results include counts of successful and failed updates.

---

## Extensibility

- New tools can be created for additional languages by implementing language-specific modules in the tools directory.
- The main codecrispr.py file dynamically loads the appropriate language tool based on file extension.
- Tools must implement a `CodeCRISPR` class with methods for reference mapping and block replacement.
- Existing tools are modular and easy to adapt for adjacent file types or custom formats.

---

## Error Handling

- File validation checks: existence, file type, and read permissions
- Safe file writing with backup and restore on failure
- Detailed error messages for common issues
- JSON output option for programmatic error handling

---

## Limitations

- Structural rather than semantic: does not parse ASTs or validate syntax
- Cannot infer edits without explicit replacement code
- Reference map depends on well-formed file structures (e.g., matching braces, consistent indentation)

---

## Summary

CodeCRISPR empowers human users and AI agents to work efficiently with large files, focusing on precise, token-efficient, targeted edits. It acts as a language-agnostic surgical editor that integrates smoothly into Claude workflows through MCP or direct local CLI use.

---

## Usage Examples

Below are practical examples of how each major feature of CodeCRISPR is used, including the exact commands and typical outputs.

---

### 1. Inspecting a File for Function Names

**Command:**

```bash
python3 codecrispr.py math_utils.py --inspect
```

**Output:**

```
Inspecting 'math_utils.py' [python_tool]:
  add: lines 3–6
  subtract: lines 8–11
  multiply: lines 13–18
```

This tells you that three functions are found in the file, with the exact line ranges.

---

### 2. Previewing a Function's Content

**Command:**

```bash
python3 codecrispr.py math_utils.py --inspect --preview "add"
```

**Output:**

```python
def add(a, b):
    return a + b
```

This extracts and shows the content of the `add` function without printing the rest of the file.

---

### 3. Previewing Changes Before Applying

**Command:**

```bash
python3 codecrispr.py math_utils.py "add" "def add(a, b):
    return a - b" --preview-changes
```

**Output:**

```
[PREVIEW] Changes to 'add':
--- original
+++ modified
@@ -1,2 +1,2 @@
 def add(a, b):
-    return a + b
+    return a - b

[INFO] Use --apply to apply these changes
```

This shows a preview of the changes without modifying the file.

---

### 4. Applying Changes After Preview

**Command:**

```bash
python3 codecrispr.py math_utils.py "add" "def add(a, b):
    return a - b" --preview-changes --apply
```

**Output:**

```
[PREVIEW] Changes to 'add':
--- original
+++ modified
@@ -1,2 +1,2 @@
 def add(a, b):
-    return a + b
+    return a - b

[UPDATED] Block 'add' replaced successfully.
```

This previews and then applies the changes.

---

### 5. Performing a Batch Update

**Batch File (`updates.json`):**

```json
{
  "updates": [
    {
      "method": "add",
      "code": "def add(a, b):\n    return a * b"
    },
    {
      "method": "multiply",
      "code": "def multiply(a, b):\n    return a + b"
    }
  ]
}
```

**Command:**

```bash
python3 codecrispr.py math_utils.py --batch updates.json
```

**Output:**

```
[SUCCESS] Updated 2 methods: add, multiply
```

---

### 6. Configuring CodeCRISPR Settings

**Command to show all settings:**

```bash
python3 codecrispr.py --config show_all
```

**Output:**

```
[general]
  backup_enabled = true
  backup_extension = .bak
  default_language = python_tool
  auto_format = false
[output]
  use_colors = true
  json_pretty = true
  show_line_numbers = false
[editor]
  tab_size = 4
  use_spaces = true
  trim_trailing_whitespace = true
```

**Command to change a setting:**

```bash
python3 codecrispr.py --config general.backup_enabled=false
```

**Output:**

```
[CONFIG] Set general.backup_enabled = false
```

---

### 7. Error Handling Example

**Command:**

```bash
python3 codecrispr.py math_utils.py "nonexistent" "def f(): pass"
```

**Output:**

```
[ERROR] Method 'nonexistent' not found.
```

This prevents unintended modifications and provides a clear, machine-readable error.

---

### 8. Using JSON Output for Integration

**Command:**

```bash
python3 codecrispr.py math_utils.py --inspect --json
```

**Output:**

```json
{
  "file": "math_utils.py",
  "language": "python_tool",
  "blocks": {
    "add": {
      "start": 3,
      "end": 6,
      "lines": 4
    },
    "subtract": {
      "start": 8,
      "end": 11,
      "lines": 4
    },
    "multiply": {
      "start": 13,
      "end": 18,
      "lines": 6
    }
  }
}
```

This format is easy to parse and use in automated workflows.

---

### 9. Exporting a Preview to a File

**Command:**

```bash
python3 codecrispr.py math_utils.py --inspect --preview "add" --export add_function.py
```

**Output:**

```
[SUCCESS] Preview exported to add_function.py
```

This saves the preview content to a separate file for reference.

---

### 10. Performance in Large Files

For files with 10,000+ lines, you can still run:

```bash
python3 codecrispr.py large_file.py --inspect
```

The result will return the reference map within milliseconds, allowing Claude or a user to continue working without delay.

---

This section demonstrates how CodeCRISPR operations look and behave in real usage, helping both humans and AI agents to interact confidently with the system.