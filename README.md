# CodeCRISPR: Precise Code Editing Framework

Save your tokens with CodeCRISPR and MCP in Claude Desktop. 

CodeCRISPR is a lightweight, language-agnostic framework that enables precise, targeted code modifications optimized for LLM-assisted development workflows. Like its biological namesake, CodeCRISPR allows for surgical edits to specific functions or code blocks without touching the rest of your codebase and without repeated token waste.

See the [narrative overview of CodeCRISPR](docs/guides/narrative_overview.md) for a comprehensive explanation.

## A Token Efficiency Advantage

### Why Every Token Matters

When working with AI assistants like Claude, you have a limited number of tokens (think of them as conversation credits) per session. CodeCRISPR is specifically designed to maximize the value of every token you spend.

### Traditional Approach vs. CodeCRISPR Efficiency

**Without CodeCRISPR:**
- Claude reads entire file (uses tokens)
- You ask for a change (minimal tokens)
- Claude either:
  - rewrites entire file to make changes (uses more tokens), or
  - rewrites the segement you want to change in its original format as a search string (uses more tokens), then writes the part you want to change in its updated format (uses even more tokens)
- Multiple operations = Multiple full file reads and writes or segment writes and rewrites

**With CodeCRISPR:**
- Claude inspects file once (builds a map)
- You ask for a change (minimal tokens)
- Subsequent changes use the map (modest tokens)
- Only changed segment content is transmitted (modest tokens)
- Multiple operations = Single inspection + efficient updates

### The "Inspect Once, Edit Many" Pattern

```text
# Inefficient (what to avoid):
# For each edit: inspect → preview → edit → verify
# Uses approximately 4x the tokens per edit

# Efficient (recommended):
# First: One inspection of the file
# Then: Direct edits using the reference map
# Result: 75%+ token savings on subsequent edits
```

### Real Token Savings Example

Consider a 1,000-line file with 10 functions to update:

- Traditional approach: ~10,000 tokens (read entire file 10 times)
- CodeCRISPR approach: ~1,500 tokens (read once, update 10 functions)
- **Savings: 85% fewer tokens used!**

## Key Features

- **Surgical Precision**: Edit specific functions or code blocks without rewriting entire files
- **Language Agnostic**: Supports Python, JavaScript, TypeScript, HTML, CSS, PHP, Rust, C++, R, MATLAB, LaTeX, SPSS, and Markdown
- **Zero Dependencies**: Pure Python implementation using only standard library
- **LLM Optimized**: Designed for efficient use with Claude and other LLMs via MCP
- **Performance Focused**: Single-parse efficiency with minimal memory overhead
- **Safe Operations**: Automatic backup creation before modifications
- **JSON Integration**: Machine-readable output for toolchain integration
- **Batch Operations**: Update multiple methods in a single command
- **Configuration Support**: Customizable behavior via config file

## Quick Start

### Prerequisites

- Python 3.8+
- macOS (for MCP integration with Claude Desktop)

### Installation

1a. Download and unzip the [CodeCRISPR.zip file](zip/CodeCRISPR.zip), 

OR

1b. Clone or copy the CodeCRISPR directory to your local `~/path/to/your/mcp/directory/`; maybe you call this directory `ClaudeMCP`.  

For example:

```bash
cp -r ~/Downloads/CodeCRISPR ~/path/to/your/mcp/directory/CC
```
OR
```bash
cp -r /path/to/codecrispr ~/path/to/your/mcp/directory/CC
```

2. Configure Claude Desktop to allow MCP access to your `ClaudeMCP` directory.

3. (Optional) Install shell completions:

```bash
python3 CC/tools/completion.py
```

4. Provide Instructions to Claude via `Settings → Profile → Personal Preferences`:

```text
# AI Instructions for CodeCRISPR Usage via MCP

## Priority Directive: Token Efficiency

When working with code files through MCP, **ALWAYS** use the CodeCRISPR framework located at `/CC/codecrispr.py` in the user's Claude MCP directory. This tool dramatically reduces token consumption by avoiding repeated full-file reads.

ENSURE YOU READ AND FOLLOW THE INSTRUCTIONS FOR AI USING CodeCRISPR found at the following path via the MCP server:
`/CC/docs/ai_instructions/ai_instructions_for_codecrispr_usage_via_mcp.md`
```

5. For complex code with special characters, always use the file-based input approach as described in the [File-Based Input section](#file-based-input-the-recommended-approach-for-complex-code).

### Backup Your Files

> ⚠️ **Warning**
> > CodeCRISPR has been very successful when used in conjunction with the Claude Desktop app for MacOS and the Model Context Protocol (MCP), but please back up your files before working on them with CodeCRISPR.  CodeCRISPR IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. 
>
> > As a built-in feature, if `backup_enabled` is set to its default of `true` and multiple updates are applied to the same file, CodeCRISPR will create sequentially numbered `.bak` files to avoid overwriting previous backups. Nevertheless, please backup your own files.

### Basic Usage

#### Inspect a File

```bash
python3 CC/codecrispr.py yourfile.py --inspect
```

#### Modify a Function

```bash
python3 CC/codecrispr.py yourfile.py function_name 'new code here'
```

#### Preview a Function

```bash
python3 CC/codecrispr.py yourfile.py --inspect --preview function_name
```

### Edit a Markdown Section

```bash
python3 CC/codecrispr.py documentation.md "Installation Guide" '## Installation Guide

Updated installation instructions here.
'
```

## File-Based Input: The Recommended Approach for Complex Code

When working with CodeCRISPR, handling complex code strings containing special characters (quotes, backslashes, dollar signs, etc.) can be challenging due to shell interpretation. Instead of struggling with escape sequences, use the file-based approach for greater reliability.

### Why Use File-Based Input?

1. **Avoid Shell Escaping Nightmares**: No need to worry about different shell escaping rules
2. **Preserve Exact Formatting**: Line breaks, indentation, and whitespace remain intact
3. **Support for Special Characters**: Easily handle quotes, dollars, backslashes, and other special characters
4. **Cross-Platform Compatibility**: Works consistently across different shells and operating systems
5. **Improved Readability**: Keep your code clean and readable without escape sequences

### File-Based Input Example

```bash
# Instead of this complex escaping (UNRELIABLE):
python3 CC/codecrispr.py file.js methodName 'const selector = element.querySelector("[id$=\\"value\\"]");'

# Use this file-based approach (RELIABLE):
cat > method_fix.js << 'EOF'
function methodName() {
    const selector = element.querySelector('[id$="-value"]');
    return selector?.textContent || '';
}
EOF

python3 CC/codecrispr.py file.js methodName "$(cat method_fix.js)"
```

### When to Use File-Based Input

Always use this approach when your replacement code contains:
- Multiple types of quotes (single, double)
- Special characters ($, \\, `, etc.)
- Multi-line content with preserved indentation
- Complex formatting that needs to be maintained exactly

This reliable approach eliminates the most common sources of errors when using CodeCRISPR and is strongly recommended for all but the simplest code replacements.
### Advanced Usage

#### JSON Output

```bash
python3 CC/codecrispr.py yourfile.py --inspect --json
```

#### Preview Changes Before Applying

```bash
python3 CC/codecrispr.py yourfile.py function_name 'new code' --preview-changes
python3 CC/codecrispr.py yourfile.py function_name 'new code' --apply
```

#### Batch Updates

```bash
python3 CC/codecrispr.py yourfile.py --batch updates.json
```

See [docs/examples/batch_update_example.json](docs/examples/batch_update_example.json) for the batch file format.

#### Configuration

```bash
# Show all configuration
python3 CC/codecrispr.py --config

# Get specific value
python3 CC/codecrispr.py --config general.backup_enabled

# Set configuration value
python3 CC/codecrispr.py --config general.backup_enabled=false
```

Configuration file is stored at `~/.codecrispr/config.ini`

## Supported Languages

| Language | File Extensions | Parser Type |
|----------|-----------------|-------------|
| C++ | .cpp, .cxx, .cc, .h, .hpp | Pattern-based |
| CSS | .css, .scss, .less | Block-based |
| Go | .go | Pattern-based |
| HTML | .html, .htm | Tag-based |
| Java | .java | Pattern-based |
| JavaScript | .js, .mjs, .cjs, .jsx | Pattern-based |
| JSON | .json | Named-key-based |
| Julia | .jl | Pattern-based |
| LaTeX | .tex | Environment-based |
| Markdown | .md | Heading-based |
| MATLAB | .m | Pattern-based     |
| PHP | .php, .php3-5, .phtml | Pattern-based |
| Python | .py, .pyw, .pyi | Indentation-based |
| R | .r, .R | Pattern-based |
| Rust | .rs | Pattern-based |
| Shell Scripts | .sh, .bash | Block-based |
| SPSS | .sps, .spss | Block-based |
| SQL | .sql | Pattern-based |
| SVG | .svg | Tag-based |
| Swift | .swift | Pattern-based |
| TypeScript | .ts, .tsx | Pattern-based |
| XML | .xml | Tag-based |

> **Note on Language Parsing Limitations**: Each language parser has specific limitations and edge cases. 
> For detailed information about these limitations and recommended workarounds,
> refer to the language-specific guides in the docs/tool_guides directory.

### Parser Types
- Pattern-based refers to tools that use regular expressions to identify function or method patterns (e.g., Java, Rust, Go).
- Block-based is used for languages where logical units are enclosed in braces or similar delimiters without formal declaration syntax (e.g., CSS, Shell, SPSS).
- Tag-based fits languages like HTML and XML that rely on nested, named tag structures.
- Named-key-based (JSON) reflects hierarchical object/array traversal via named keys.
- Environment-based (LaTeX) uses \\begin{...} and \\end{...} to delimit sections.
- Heading-based (Markdown) uses section titles with # symbols.
- Indentation-based (Python) depends on whitespace to define scope.

## Documentation

- [A Comprehensive Explanation of CodeCRISPR](docs/guides/narrative_overview.md) - A detailed narrative overview of all that is CodeCRiSPER, for those who like to read
- [Novice User Guide](docs/guides/novice_user_guide.md) - Friendly introduction for new users
- [Advanced Technical Guide](docs/guides/advanced_technical_guide.md) - Deep dive into architecture and extension
- [CodeCRISPR Features Guide](docs/guides/codecrispr_features.md) - Information about features under-the-hood
- [Customization Guide](docs/guides/customization.md) - Information about cutomizing via the INI file
- [Language-Specific Caveats](docs/guides/language_caveats.md) - Important limitations and workarounds for each supported language
- [Error Handling Guide](docs/guides/error_handling_guide.md) - Detailed troubleshooting guide for common error scenarios
- Language Specific Guides
  - [C++ Tool Guide](docs/tool_guides/cpp_tool_guide.md)
  - [CSS Tool Guide](docs/tool_guides/css_tool_guide.md)
  - [Go Tool Guide](docs/tool_guides/go_tool_guide.md)
  - [HTML Tool Guide](docs/tool_guides/html_tool_guide.md)
  - [JavaScript Tool Guide](docs/tool_guides/javascript_tool_guide.md)
  - [Java Tool Guide](docs/tool_guides/java_tool_guide.md)
  - [JSON Tool Guide](docs/tool_guides/json_tool_guide.md)
  - [Julia Tool Guide](docs/tool_guides/julia_tool_guide.md)
  - [LaTeX Tool Guide](docs/tool_guides/latex_tool_guide.md)
  - [Markdown Tool Guide](docs/tool_guides/markdown_tool_guide.md)
  - [MATLAB Tool Guide](docs/tool_guides/matlab_tool_guide.md)
  - [PHP Tool Guide](docs/tool_guides/php_tool_guide.md)
  - [Python Tool Guide](docs/tool_guides/python_tool_guide.md)
  - [R Tool Guide](docs/tool_guides/r_tool_guide.md)
  - [Rust Tool Guide](docs/tool_guides/rust_tool_guide.md)
  - [Shell Tool Guide](docs/tool_guides/shell_tool_guide.md)
  - [SPSS Tool Guide](docs/tool_guides/spss_tool_guide.md)
  - [SQL Tool Guide](docs/tool_guides/sql_tool_guide.md)
  - [SVG Tool Guide](docs/tool_guides/svg_tool_guide.md)
  - [Swift Tool Guide](docs/tool_guides/swift_tool_guide.md)
  - [XML Tool Guide](docs/tool_guides/xml_tool_guide.md)
- [AI Instructions for CodeCRISPR](docs/ai_instructions/ai_instructions_for_codecrispr_usage_via_mcp.md) - Guide for AI assistants using CodeCRISPR

## But Why Not Just Use an AST?

While Abstract Syntax Trees (AST) provide a powerful and precise way to understand and manipulate code, CodeCRISPR remains a valuable tool for several reasons:
1.  **Broad Compatibility**: CodeCRISPR supports a wide range of languages and file types on its own, including those for which AST tooling might not be readily available or practical. This ensures that developers can still efficiently edit and manage their code across different technologies.
2.  **Lightweight and Flexible**: CodeCRISPR operates in a lightweight manner, making it easy to integrate into various environments. It can function independently or alongside AST tools, providing a fallback or complementary solution when AST parsing is not feasible or necessary.
3.  **Efficiency for Simple Tasks**: For many straightforward editing tasks, CodeCRISPR offers a streamlined and easy-to-use interface. Users can make quick changes without the overhead of AST processing, which can be beneficial for smaller or less complex codebases.
4.  **Efficiency for Polyglot Projects**: It may be the case that your project includes files written in several languages.  Each language requires the installation of its own respective AST application.  However, CodeCRISPR is designed to work seamlessly with projects that use multiple languages.
5.  **Extensibility**: CodeCRISPR is designed to be very extensible.  Don't see the language you use in the existing tools?  Tell us, or build your own tool and contribute it to the CodeCRISPR community.
6.  **Token Management**: Even with AST, there are scenarios where CodeCRISPR’s token-efficient design is advantageous. It reduces the token footprint by focusing on targeted, section-based edits, which is crucial in token-limited environments.
7.  **Ease of Use for Non-Technical Users**: CodeCRISPR is designed to be intuitive, making it accessible for users who may not be familiar with the intricacies of ASTs. Additionally, there is nothing to install (no package managers, neither `pip` nor `brew`, no `install`) beyond unzipping, then placing, CodeCRISPR in the CC directory at Claude's MCP access point.  Everything CodeCRISPR needs is already within MacOS's Python implementation. This ensures that a broader range of users can benefit from its capabilities.

CodeCRISPR and AST complement each other. CodeCRISPR offers a flexible, efficient, and user-friendly solution that remains valuable even when advanced AST tools are available, ensuring that developers have the right tool for every situation.

## Configuration Options

| Section | Option | Default | Description |
|---------|--------|---------|-------------|
| general | backup_enabled | true | Create backups before modifications |
| general | backup_extension | .bak | Extension for backup files |
| general | default_language | python_tool | Default language parser |
| output | use_colors | true | Enable colored output |
| output | json_pretty | true | Pretty-print JSON output |
| output | show_line_numbers | false | Show line numbers by default |
| editor | tab_size | 4 | Default tab size |
| editor | use_spaces | true | Use spaces instead of tabs |
| editor | trim_trailing_whitespace | true | Remove trailing whitespace |

## Expected Architecture

CodeCRISPR uses a modular architecture with language-specific parsers:

```
CC/
├── codecrispr.py           # Main CLI and core logic
├── tools/                  # Language-specific parsers
│   ├── python_tool.py
│   ├── javascript_tool.py
│   ├── completion.py       # Shell completion scripts
│   └── ...
└── docs/                   # Documentation
    ├── guides/
    └── examples/           # Example files
```

Each language tool implements the `CodeCRISPR` class with required methods for parsing and code replacement.

## Recent Updates

- Added support for additional langauges, including Markdown documents with heading-based section editing
- Enhanced token efficiency guidelines for AI assistants
- Enhanced error handling with file validation
- Added JSON output format for better integration
- Implemented batch operations for multiple edits
- Added diff preview before applying changes
- Improved language detection with fallback mechanisms
- Configuration file support for customization
- Shell completion for bash and zsh

## Use Cases

- **LLM-Assisted Development**: Efficient code modifications with Claude
- **Targeted Refactoring**: Update specific functions without full-file rewrites
- **Documentation Management**: Edit markdown document sections by headings
- **Code Review**: Extract and examine specific code blocks
- **Automated Code Updates**: Programmatic code modifications
- **CI/CD Integration**: JSON output enables seamless toolchain integration
- **Batch Processing**: Update multiple files and functions in automation scripts

### Complex JavaScript Method Update

Using the file-based input approach for a complex JavaScript method with special characters:

```bash
# Create temporary file with the exact code
cat > new_render_method.js << 'EOF'
render() {
  const element = document.querySelector('#app');
  const data = this.state.items.map(item => `
    <li class="item" data-id="${item.id}">
      <h3>${item.name}</h3>
      <p>${item.description}</p>
      ${item.isSpecial ? '<span class="special">★</span>' : ''}
    </li>
  `).join('');
  
  element.innerHTML = `<ul class="items">${data}</ul>`;
  
  // Add event listeners
  document.querySelectorAll('[data-id]').forEach(el => {
    el.addEventListener('click', () => this.handleClick(el.dataset.id));
  });
}
EOF

# Use command substitution to pass the content
python3 CC/codecrispr.py app.js render "$(cat new_render_method.js)"
```

This approach ensures that all template literals, quotes, and special characters are preserved exactly as written without requiring complex escape sequences.

## Performance

CodeCRISPR is designed for efficiency:

- Single file parse on initialization
- O(1) lookups for method locations
- Incremental offset updates after edits
- No external dependencies or heavy frameworks
- Minimal memory footprint

## License

Modified MIT License - See [LICENSE](LICENSE) file for details

## Contributing

To add support for a new language:

1. Create a new tool file in `tools/[language]_tool.py`
2. Implement the `CodeCRISPR` class with required methods
3. Add the file extension mapping in `codecrispr.py`

See the [Advanced Technical Guide](docs/guides/advanced_technical_guide.md) for detailed implementation instructions.

## Troubleshooting

### Backup Your Files

> ⚠️ **Warning**
> > CodeCRISPR has been very successful when used in conjunction with the Claude Desktop app for MacOS and the Model Context Protocol (MCP), but please back up your files before working on them with CodeCRISPR.  CodeCRISPR IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. 
>
> >As a built-in feature, if `backup_enabled` is set to its default of `true` and multiple updates are applied to the same file, CodeCRISPR will create sequentially numbered `.bak` files to avoid overwriting previous backups. Nevertheless, please backup your own files.

### Common Error Scenarios and Solutions

#### 1. Method Not Found Errors

**Scenario**: `[ERROR] Method 'function_name' not found.`

**Potential Causes**:
- Method name misspelled
- Method exists but wasn't detected by the parser
- Method is defined dynamically or conditionally
- Method is nested inside another function/class

**Solutions**:
- Use `--inspect` to get the exact method names from the reference map
- Verify case sensitivity and exact spelling
- For nested methods, target the parent method/class instead
- Use `edit_block` as a fallback for methods that aren't being detected

#### 2. Syntax Errors After Editing

**Scenario**: The edited file contains syntax errors after using CodeCRISPR.

**Potential Causes**:
- Incorrect indentation in the replacement code
- Missing parentheses, braces, or other syntax elements
- Inconsistent line endings (CRLF vs LF)
- Invisible/non-printing characters in the replacement code

**Solutions**:
- Use `--preview-changes` before applying changes to verify syntax
- Ensure consistent indentation matching the file's style
- Check for balanced parentheses, braces, and quotation marks
- Use the file-based input approach to avoid shell interpretation issues
- Run a syntax validator after editing (e.g., `python -m py_compile` for Python files)

#### 3. File Permission Errors

**Scenario**: `[ERROR] Failed to write file: Permission denied`

**Potential Causes**:
- The file is read-only
- The file is owned by another user
- The file is locked by another process
- The file is in a directory with restricted permissions

**Solutions**:
- Check file permissions with `ls -l <filepath>`
- Change permissions with `chmod u+w <filepath>`
- Close any applications that might have the file open
- Copy the file to a location with appropriate permissions, edit there, then move back

#### 4. Command Line Escaping Issues

**Scenario**: Arguments containing special characters aren't interpreted correctly.

**Potential Causes**:
- Shell interpretation of quotes, variables, or escape sequences
- Backticks being interpreted as command substitution
- Dollar signs being interpreted as variable references
- Newlines or tabs in the replacement code

**Solutions**:
- Use the file-based input approach for complex replacement code as described in the [File-Based Input section](#file-based-input-the-recommended-approach-for-complex-code)

#### 5. Parser Detection Issues

**Scenario**: CodeCRISPR fails to correctly identify functions or sections in the file.

**Potential Causes**:
- Unusual coding style or non-standard syntax
- Mixed language content in a single file
- The file type isn't correctly detected
- The language parser has limitations for certain constructs

**Solutions**:
- Use an explicit language tool via the config if detection fails
- Format the code with a standard formatter before editing
- Use simpler, more standard syntax for problematic code sections
- Split mixed-language files into separate files if possible
- Use `edit_block` for sections that aren't properly detected

### Getting Help

- Check the documentation in the `docs/` directory
- Review examples in `docs/examples/`
- Submit issues on the project repository

## Roadmap

- [ ] Add support for more languages
- [ ] Implement semantic code analysis
- [ ] Add Git integration for automatic commits
- [ ] Create VS Code extension
- [ ] Add web interface for visual editing
- [ ] Implement code formatting integration

## Version History

- **1.2.3** - Added support for SQL, SVG, Julia, shell scripts, JSON, XML, and Java editing with respective tools.
- **1.2.2** - Added support for go and swift editing with go_tool.py and swift_tool.py
- **1.2.1** - Added support for markdown editing with markdown_tool.py
- **1.2.0** - Added batch operations, JSON output, configuration support
- **1.1.0** - Enhanced language parsers for modern syntax
- **1.0.0** - Initial release with core functionality
