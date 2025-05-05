# AI Instructions for CodeCRISPR Usage via MCP

## Priority Directive: Token Efficiency

When working with code files through MCP, **ALWAYS** use the CodeCRISPR framework located at `/CC/codecrispr.py` in the user's Claude MCP directory. This tool dramatically reduces token consumption by avoiding repeated full-file reads.

## Core Principles

1. **Inspect Once, Edit Many**: After initial file inspection, use the cached reference map for all subsequent operations
2. **Direct Edits Over Previews**: Only preview when you genuinely need to see current content
3. **Batch Operations**: Plan and execute multiple related changes after a single inspection
4. **Trust the Tool**: CodeCRISPR accurately targets specific functions/methods - verification previews waste tokens
5. **Use JSON Output**: For integration with other tools, use `--json` flag for machine-readable output
6. **Configuration Awareness**: Check configuration with `--config` before operations that might be affected

## Standard Operating Procedure

### 1. Initial File Assessment

When first encountering any code file:

```bash
# Always use python3, NOT python
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> --inspect
```

Store the reference map mentally. This is your roadmap for all subsequent operations.

### 2. Direct Edit Pattern (Preferred)

For any function/method modifications:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> <method_name> '<new_code>'
```

**DO NOT** preview before editing if you already know the function structure.
**DO NOT** preview after editing to verify - trust the "[UPDATED]" confirmation.

### 3. Preview Only When Necessary

Use preview ONLY when:
- You genuinely need to see current function implementation
- The user specifically requests to see the code
- You're unsure about function boundaries or structure

```bash
# Use sparingly
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> --inspect --preview <method_name>
```

### 4. Batch Operations (New Feature)

For multiple updates in a single file:

```bash
# Create a batch file
cat > updates.json << 'EOF'
{
  "updates": [
    {"method": "function1", "code": "def function1(): pass"},
    {"method": "function2", "code": "def function2(): pass"}
  ]
}
EOF

# Apply batch updates
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> --batch updates.json
```

### 5. Preview Changes Before Applying

When you want to see what will be changed:

```bash
# Preview changes
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> <method_name> '<new_code>' --preview-changes

# If satisfied, apply the changes
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> <method_name> '<new_code>' --apply
```

## Supported File Types

CodeCRISPR automatically detects language by extension:
- C++ (.cpp, .cxx, .cc, .h, .hpp)
- CSS (.css, .scss, .less)
- Go (.go)
- HTML (.html, .htm)
- Java (.java)
- JavaScript (.js, .mjs, .cjs, .jsx)
- JSON (.json)
- Julia (.jl)
- LaTeX (.tex)
- Markdown (.md)
- MATLAB (.m)
- PHP (.php, .php3-5, .phtml)
- Python (.py, .pyw, .pyi)
- R (.r, .R)
- Rust (.rs)
- Shell (.sh, .bash)
- SPSS (.sps, .spss)
- SQL (.sql)
- SVG (.svg)
- Swift (.swift)
- TypeScript (.ts, .tsx)
- XML (.xml)

## Configuration Management

Check or modify configuration:

```bash
# Show all configuration
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py --config

# Check specific value
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py --config general.backup_enabled

# Set configuration value
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py --config general.backup_enabled=false
```

## JSON Output for Integration

Use JSON output for machine-readable results:

```bash
# Get file structure as JSON
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> --inspect --json

# Parse with jq for specific information
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py <filepath> --inspect --json | jq '.blocks | keys[]'
```

## Workflow Examples

### Efficient Multi-Function Edit Workflow

```python
# Step 1: Single inspection
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py project/main.py --inspect")
# Store reference map: main(), helper(), calculate(), render()

# Step 2: Direct edits without previews
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py project/main.py main '<new_main_code>'")
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py project/main.py helper '<new_helper_code>'")
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py project/main.py calculate '<new_calculate_code>'")

# Total token cost: 1 inspection + 3 minimal edits (vs. 3 full file reads in traditional approach)
```

### Batch Update Workflow

```python
# Step 1: Create batch update file
batch_data = {
    "updates": [
        {"method": "parse_data", "code": "def parse_data(input):\n    return json.loads(input)"},
        {"method": "validate_data", "code": "def validate_data(data):\n    return bool(data)"},
        {"method": "process_data", "code": "def process_data(data):\n    return data.upper()"}
    ]
}
execute_command(f"echo '{json.dumps(batch_data)}' > batch_updates.json")

# Step 2: Apply batch updates
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py data_processor.py --batch batch_updates.json")
```

### Preview-and-Apply Workflow

```python
# When unsure about changes
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py file.py function_name '<new_code>' --preview-changes")
# Review the diff output
execute_command("cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py file.py function_name '<new_code>' --apply")
```

### Avoid These Anti-Patterns 

```python
# INEFFICIENT - Don't do this:
execute_command("cd ... && python3 CC/codecrispr.py file.py --inspect")
execute_command("cd ... && python3 CC/codecrispr.py file.py --inspect --preview function1")
execute_command("cd ... && python3 CC/codecrispr.py file.py function1 '<code>'")
execute_command("cd ... && python3 CC/codecrispr.py file.py --inspect --preview function1")  # Unnecessary verification

# EFFICIENT - Do this instead:
execute_command("cd ... && python3 CC/codecrispr.py file.py --inspect")
execute_command("cd ... && python3 CC/codecrispr.py file.py function1 '<code>'")
```

## Error Handling

If you encounter errors:

1. Check if using `python3` instead of `python`
2. Verify file path is correct and within allowed directories
3. Ensure method name exactly matches the reference map
4. Properly escape quotes in replacement code
5. Check configuration if backup fails (`--config general.backup_enabled`)
6. Verify JSON format for batch operations
7. Consider using file-based input for complex code (see next section)

## Handling Complex String Arguments

### The File-Based Approach for Complex Code Replacements

When working with CodeCRISPR, complex code strings containing special characters (quotes, backslashes, dollar signs, etc.) can be problematic due to shell interpretation. This section describes a reliable approach to handle such cases.

### The Problem Pattern

1. You need to pass code containing special characters as a command-line argument
2. The shell interprets these characters, requiring complex escape sequences
3. Multiple levels of escaping create confusion and errors
4. Different shells (bash, zsh, cmd) handle escaping differently

### Recommended Solution: File-Based Input

Instead of struggling with shell escaping:

1. Write the complex code to a temporary file
2. Use command substitution (`$(cat filename)`) to pass the content
3. This bypasses shell interpretation issues entirely

```bash
# Instead of complex escaping:
codecrispr file.js methodName 'const selector = element.querySelector("[id$=\"-value\"]");'

# Use file-based approach:
cat > method_fix.js << 'EOF'
const selector = element.querySelector('[id$="-value"]');
EOF
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py file.js methodName "$(cat method_fix.js)"
```

### When to Use This Approach

1. **Complex Code Snippets**: When the code contains multiple types of quotes, backslashes, or shell metacharacters
2. **Multi-line Content**: When the replacement code spans multiple lines with varying indentation
3. **Cross-Platform Compatibility**: When the same command needs to work across different shells/OS
4. **Generated or Dynamic Content**: When the content is programmatically generated
5. **Maintenance and Readability**: When the escaped command becomes too complex to read

### Implementation Examples

```bash
# Example 1: JavaScript with complex selectors
cat > querySelector_fix.js << 'EOF'
    querySelector('[data-attr="value"]') {
        const element = document.querySelector('[id$="-value"]');
        return element?.textContent || '';
    }
EOF
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py component.js querySelector "$(cat querySelector_fix.js)"

# Example 2: Python with quotes and escapes
cat > string_handler_fix.py << 'EOF'
def handle_string(text):
    """Process text with 'single' and "double" quotes."""
    return text.replace('\\n', '\n').replace('\\"', '"')
EOF
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py utils.py handle_string "$(cat string_handler_fix.py)"
```

### Benefits

- **Reliability**: Eliminates shell interpretation issues
- **Readability**: Code remains readable without escape sequences
- **Version Control**: File-based updates can be tracked
- **Reusability**: The same file can be used for multiple operations
- **Testing**: Easier to validate content before applying

### Best Practices

1. Use heredoc syntax with quoted delimiter (`<< 'EOF'`) to prevent shell expansion
2. Name temporary files descriptively (e.g., `methodName_fix.js`)
3. Clean up temporary files after use if needed
4. Consider creating a dedicated directory for fix files in larger projects

This approach trades a small amount of setup complexity for significant reliability gains, especially when dealing with code containing special characters or when working across different environments.
## Performance Guidelines

| File Size | Expected Parse Time | Subsequent Edit Time |
|-----------|-------------------|---------------------|
| < 1K lines | ~10ms | ~5ms |
| 1K-10K lines | ~100ms | ~10ms |
| 10K+ lines | ~1s | ~20ms |

## Special Considerations

1. **Large Files**: For files > 1000 lines, the initial inspection investment pays off even more
2. **String Escaping**: Use double quotes for the command and escape internal quotes properly
3. **Multi-line Code**: Preserve formatting in replacement code, including proper indentation
4. **Session Persistence**: Reference maps persist throughout the conversation - never re-inspect unnecessarily
5. **Backup Files**: By default, `.bak` files are created; disable with `--config general.backup_enabled=false`
6. **JSON Pretty Print**: Control JSON formatting with `--config output.json_pretty=false`

## Decision Tree for CodeCRISPR Operations

```
Start with new file?
├─ YES → Inspect once → Store reference map
└─ NO → Use existing reference map

Need to edit function?
├─ Know structure? → Direct edit (no preview)
└─ Unsure? → Preview once → Edit

User requests to see code?
└─ YES → Use preview with appropriate flags

Multiple edits needed?
├─ YES → Consider batch operation
└─ NO → Single edit operation

Need machine-readable output?
└─ YES → Use --json flag
```

## Token Savings Formula

For n edits on a file of size L lines:
- Traditional approach: n × L tokens
- CodeCRISPR approach: L + (n × 10) tokens
- Savings: (n × L - L - n × 10) / (n × L) ≈ 90%+ for n > 1

## Integration with Other MCP Tools

CodeCRISPR works alongside other MCP file operations:
- Use CodeCRISPR for function-level edits
- Use `write_file` for complete file rewrites
- Use `read_file` only when CodeCRISPR isn't applicable
- Combine CodeCRISPR with `search_code` for targeted refactoring
- Use JSON output to pipe results to other tools

## Key Reminders

1. **ALWAYS** check for CodeCRISPR availability before defaulting to read_file/write_file
2. **NEVER** re-inspect files unless structure has changed
3. **AVOID** preview operations unless absolutely necessary
4. **TRUST** CodeCRISPR's surgical precision
5. **BATCH** related edits for maximum efficiency
6. **USE** configuration to customize behavior
7. **LEVERAGE** JSON output for tool integration

## Token-Efficient Implementation Guidelines

Follow these guidelines to make more token-efficient choices when using CodeCRISPR:

1. **Explicit CodeCRISPR Directive**: When modifying entire methods or functions, always use CodeCRISPR's direct method replacement rather than edit_block. Only use edit_block for partial file changes that don't correspond to complete methods.

2. **Function Boundary Awareness**: Be aware that CodeCRISPR can accurately identify function boundaries. When you need to modify a function, trust CodeCRISPR to correctly replace only that function without needing to specify the exact start and end lines.

3. **Tool Selection Hierarchy**: Follow this hierarchy for file modifications: 
   - For copying existing files: Use the cp command
   - For modifying entire functions: Use CodeCRISPR method replacement
   - For targeted, non-function edits: Use edit_block
   - For creating new files: Use write_file

4. **Batch Operations Guidance**: When multiple functions need to be modified, consider using CodeCRISPR's batch operation capability rather than making multiple individual edits.

## Markdown Tool Usage

The Markdown tool extends CodeCRISPR's capabilities to efficiently edit markdown documents by sections. It recognizes markdown heading structures (using # syntax) and allows precise replacement of entire sections.

### Markdown-Specific Features

- **Section-Based Editing**: Replace entire sections (heading + content) with a single operation
- **Heading Hierarchy Awareness**: Understands the document structure based on heading levels (# vs ## vs ###)
- **Preservation of Document Structure**: Maintains the overall document organization while updating specific sections

### Example Markdown Workflow

```bash
# Inspect markdown document structure
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md --inspect

# Replace a specific section
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md "Installation Guide" '## Installation Guide

Follow these steps to install the application:

1. Download the latest release
2. Extract the files to your desired location
3. Run the setup script
4. Configure your settings
'
```

By following these instructions, you'll achieve 80-95% token savings on typical code editing tasks while maintaining precision and reliability.
