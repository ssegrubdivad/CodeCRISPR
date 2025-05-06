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
- Each replacement operation generates a **Git-style unified diff** that highlights:
  - Removed lines (`-`)
  - Added lines (`+`)
  - Context lines (unchanged)
- This output helps users and AI verify the exact impact of changes without printing the entire file.
- Diffs include:
  - Original and modified file labels
  - A "hunk" header showing line numbers and method name
  - Line-level changes

### Section Preview
- Users or AI agents can request to preview the **current contents of any named method or section** before deciding whether to modify it.
- This preview uses the reference map to extract only the relevant lines from the file.
- The command `--inspect --preview "method_name"` displays the code for that block only.

---

## Performance Characteristics

- **Initial parse** is O(n) where n is the number of lines.
- **Subsequent operations** (e.g., replacement, preview) are constant time (O(1)) thanks to the reference map.
- **Edits are performed in memory**, with disk writes only when explicitly saved.
- **Incremental map updates** allow efficient management of large files, up to tens of thousands of lines.

---

## File Types and Parsers

Each supported file type has a dedicated parsing strategy:
- Python: Indentation-based
- JavaScript / TypeScript / Java / Go / Rust / C++ / Julia / Swift / R: Pattern-based
- CSS / Shell / SPSS: Block-based
- HTML / XML / SVG: Tag-based
- LaTeX: Environment-based (`\begin{...}`/`\end{...}`)
- Markdown: Heading-based
- JSON: Named-key-based
- SQL: Pattern-based statement parsing

---

## Backup System

- If `backup_enabled = true`, CodeCRISPR creates `.bak` files before modification.
- Subsequent backups are numbered (`.bak`, `.bak1`, `.bak2`, ...) to avoid overwrites.
- This ensures recovery is always possible even in batch or iterative edit scenarios.

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

- CodeCRISPR supports JSON-based batch editing:
```json
{
  "updates": [
    { "method": "foo", "code": "..." },
    { "method": "bar", "code": "..." }
  ]
}
```
- This allows AI or users to edit many parts of a file efficiently in one invocation.

---

## Extensibility

- New tools can be created for additional languages by subclassing and implementing a parser for:
  - Reference mapping
  - Section identification
- Existing tools are modular and easy to adapt for adjacent file types or custom formats.

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
  - add: lines 3–6
  - subtract: lines 8–11
  - multiply: lines 13–18
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

### 3. Replacing a Function with New Code

**Command:**

```bash
python3 codecrispr.py math_utils.py "add" "def add(a, b):
    return a - b"
```

**Output (diff):**

```
--- math_utils.py
+++ math_utils.py
@@ -3,2 +3,2 @@ add
-def add(a, b):
-    return a + b
+def add(a, b):
+    return a - b
```

This confirms the replacement and shows what changed.

---

### 4. Performing a Batch Update

**Batch File (`updates.json`):**

```json
{
  "updates": [
    {
      "method": "add",
      "code": "def add(a, b):\\n    return a * b"
    },
    {
      "method": "multiply",
      "code": "def multiply(a, b):\\n    return a + b"
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
Updated method: add
Updated method: multiply
```

---

### 5. Creating and Using Backups

If backups are enabled (`backup_enabled = true`), a file like `math_utils.py.bak` is created before any change. If a backup already exists, it creates `math_utils.py.bak1`, `math_utils.py.bak2`, etc.

This protects your original file from accidental overwrites.

---

### 6. Error Handling Example

**Command:**

```bash
python3 codecrispr.py math_utils.py "nonexistent" "def f(): pass"
```

**Output:**

```
ERROR: Function 'nonexistent' not found.
```

This prevents unintended modifications and provides a clear, machine-readable error.

---

### 7. Performance in Large Files

For files with 10,000+ lines, you can still run:

```bash
python3 codecrispr.py large_file.py --inspect
```

The result will return the reference map within milliseconds, allowing Claude or a user to continue working without delay.

---

This section demonstrates how CodeCRISPR operations look and behave in real usage, helping both humans and AI agents to interact confidently with the system.