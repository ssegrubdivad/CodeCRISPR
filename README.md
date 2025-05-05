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

```python
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

### Backup Your Files

> ⚠️ **Warning**
> > CodeCRISPR has been very successful when used in conjunction with the Claude Desktop app for MacOS and the Model Context Protocol (MCP), but please back up your files before working on them with CodeCRISPR.  CodeCRISPR IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

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

#### Edit a Markdown Section

```bash
python3 CC/codecrispr.py documentation.md "Installation Guide" '## Installation Guide

Updated installation instructions here.
'
```

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

## But Why Not Just Use an AST?

While Abstract Syntax Trees (AST) provide a powerful and precise way to understand and manipulate code, CodeCRISPR remains a valuable tool for several reasons:
1.  **Broad Compatibility**: CodeCRISPR supports a wide range of languages and file types on its own, including those for which AST tooling might not be readily available or practical. This ensures that developers can still efficiently edit and manage their code across different technologies.
2.  **Lightweight and Flexible**: CodeCRISPR operates in a lightweight manner, making it easy to integrate into various environments. It can function independently or alongside AST tools, providing a fallback or complementary solution when AST parsing is not feasible or necessary.
3.  **Efficiency for Simple Tasks**: For many straightforward editing tasks, CodeCRISPR offers a streamlined and easy-to-use interface. Users can make quick changes without the overhead of AST processing, which can be beneficial for smaller or less complex codebases.
4.  **Efficiency for Polyglot Projects**: It may be the case that your project includes files written in several languages.  Each language requires the installation of its own respective AST application.  However, CodeCRISPR is designed to work seamlessly with projects that use multiple languages.
5.  **Extensibility**: CodeCRISPR is designed to be very extensible.  Don't see the language you use in the existing tools?  Tell us, or build your own tool and contribute it to the CodeCRISPR community.
6.  **Token Management**: Even with AST, there are scenarios where CodeCRISPR’s token-efficient design is advantageous. It reduces the token footprint by focusing on targeted, section-based edits, which is crucial in token-limited environments.
7.  **Ease of Use for Non-Technical Users**: CodeCRISPR is designed to be intuitive, making it accessible for users who may not be familiar with the intricacies of ASTs. This ensures that a broader range of users can benefit from its capabilities.

CodeCRISPR and AST complement each other. CodeCRISPR offers a flexible, efficient, and user-friendly solution that remains valuable even when advanced AST tools are available, ensuring that developers have the right tool for every situation.

## Documentation

- [A Comprehensive Explanation of CodeCRISPR](docs/guides/narrative_overview.md) - A detailed narrative overview of all that is CodeCRiSPER, for those who like to read
- [Novice User Guide](docs/guides/novice_user_guide.md) - Friendly introduction for new users
- [Advanced Technical Guide](docs/guides/advanced_technical_guide.md) - Deep dive into architecture and extension
- [Customization Guide](docs/guides/customization.md) - Information about cutomizing via the INI file
- Language Specific Guides
  - [C++ Tool Guide](docs/tool_guides/cpp_tool_guide.md)
  - [CSS Tool Guide](docs/tool_guides/css_tool_guide.md)
  - [Go Tool Guide](docs/tool_guides/go_tool_guide.md)
  - [HTML Tool Guide](docs/tool_guides/html_tool_guide.md)
  - [JavaScript Tool Guide](docs/tool_guides/javascript_tool_guide.md)
  - [LaTeX Tool Guide](docs/tool_guides/latex_tool_guide.md)
  - [Markdown Tool Guide](docs/tool_guides/markdown_tool_guide.md)
  - [MATLAB Tool Guide](docs/tool_guides/matlab_tool_guide.md)
  - [PHP Tool Guide](docs/tool_guides/php_tool_guide.md)
  - [Python Tool Guide](docs/tool_guides/python_tool_guide.md)
  - [R Tool Guide](docs/tool_guides/r_tool_guide.md)
  - [Rust Tool Guide](docs/tool_guides/rust_tool_guide.md)
  - [SPSS Tool Guide](docs/tool_guides/spss_tool_guide.md)
  - [Swift Tool Guide](docs/tool_guides/swift_tool_guide.md)
- [AI Instructions for CodeCRISPR](docs/ai_instructions/ai_instructions_for_codecrispr_usage_via_mcp.md) - Guide for AI assistants using CodeCRISPR

## Supported Languages

| Language | File Extensions | Parser Type |
|----------|-----------------|-------------|
| C++ | .cpp, .cxx, .cc, .h, .hpp | Pattern-based |
| CSS | .css, .scss, .less | Block-based |
| Go | .go | Pattern-based |
| HTML | .html, .htm | Tag-based |
| JavaScript | .js, .mjs, .cjs, .jsx | Pattern-based |
| LaTeX | .tex | Environment-based |
| Markdown | .md | Heading-based |
| MATLAB | .m | Pattern-based     |
| PHP | .php, .php3-5, .phtml | Pattern-based |
| Python | .py, .pyw, .pyi | Indentation-based |
| R | .r, .R | Pattern-based |
| Rust | .rs | Pattern-based |
| SPSS | .sps, .spss | Block-based |
| Swift | .swift | Pattern-based |
| TypeScript | .ts, .tsx | Pattern-based |

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

## Architecture

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

- Added support for Markdown documents with heading-based section editing
- Enhanced token efficiency guidelines for AI assistants
- Enhanced error handling with file validation
- Added JSON output format for better integration
- Implemented batch operations for multiple edits
- Added diff preview before applying changes
- Improved language detection with fallback mechanisms
- Configuration file support for customization
- Shell completion for bash and zsh

## Contributing

To add support for a new language:

1. Create a new tool file in `tools/[language]_tool.py`
2. Implement the `CodeCRISPR` class with required methods
3. Add the file extension mapping in `codecrispr.py`

See the [Advanced Technical Guide](docs/guides/advanced_technical_guide.md) for detailed implementation instructions.

## Use Cases

- **LLM-Assisted Development**: Efficient code modifications with Claude
- **Targeted Refactoring**: Update specific functions without full-file rewrites
- **Documentation Management**: Edit markdown document sections by headings
- **Code Review**: Extract and examine specific code blocks
- **Automated Code Updates**: Programmatic code modifications
- **CI/CD Integration**: JSON output enables seamless toolchain integration
- **Batch Processing**: Update multiple files and functions in automation scripts

## Performance

CodeCRISPR is designed for efficiency:

- Single file parse on initialization
- O(1) lookups for method locations
- Incremental offset updates after edits
- No external dependencies or heavy frameworks
- Minimal memory footprint

## License

Modified MIT License - See [LICENSE](LICENSE) file for details

## Credits

CodeCRISPR was designed to optimize LLM-assisted code editing workflows, particularly with Anthropic's Claude via the Model Context Protocol (MCP). The framework demonstrates how targeted code editing can dramatically reduce token usage while improving reliability.

## Troubleshooting

### Backup Your Files

> ⚠️ **Warning**
> > CodeCRISPR has been very successful when used in conjunction with the Claude Desktop app for MacOS and the Model Context Protocol (MCP), but please back up your files before working on them with CodeCRISPR.  CodeCRISPR IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

### Common Issues

1. **Permission Errors**: Ensure the file has write permissions
2. **Parser Not Found**: Check that the file extension is supported
3. **Method Not Found**: Use `--inspect` to see available methods
4. **JSON Parse Errors**: Validate your batch JSON file format

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

- **1.2.2** - Added support for go and swift editing with go_tool.py and swift_tool.py
- **1.2.1** - Added support for markdown editing with markdown_tool.py
- **1.2.0** - Added batch operations, JSON output, configuration support
- **1.1.0** - Enhanced language parsers for modern syntax
- **1.0.0** - Initial release with core functionality
