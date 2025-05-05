# Markdown Tool Guide

## Introduction

The Markdown Tool extends CodeCRISPR's functionality to support efficient section-based editing of Markdown documents. This guide covers how to use the tool effectively for common Markdown editing workflows.

## How the Markdown Tool Works

Unlike traditional code-based tools that focus on functions or methods, the Markdown tool:

1. **Parses Headings**: Identifies all headings in a Markdown document (lines starting with # symbols)
2. **Maps Document Structure**: Creates a reference map of each section (a heading and its content)
3. **Enables Section Replacement**: Allows replacing entire sections while preserving document structure

## Core Features

- **Section-Based Editing**: Replace entire sections (heading + content) with a single operation
- **Heading Hierarchy Awareness**: Understands nested heading levels (# vs ## vs ###)
- **Document Structure Preservation**: Maintains overall document organization while updating sections
- **Batch Operations Support**: Update multiple sections in a single operation

## Basic Usage Workflow

### 1. Inspect Document Structure

First, inspect the Markdown document to understand its structure:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md --inspect
```

Output will show all headings with their line ranges:
```
Inspecting 'documentation.md' [markdown_tool]:
  # Project Documentation: lines 0–2
  ## Installation: lines 3–10
  ## Usage: lines 11–15
  ### Basic Commands: lines 16–20
  ### Advanced Features: lines 21–30
  ## Troubleshooting: lines 31–40
```

### 2. Preview a Section (if needed)

To see the content of a specific section:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md --inspect --preview "Installation"
```

### 3. Replace a Section

To replace an entire section:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md "Installation" '## Installation

Follow these steps to install the application:

1. Download the latest release
2. Extract the files to your desired location
3. Run the setup script
4. Configure your settings
'
```

## Advanced Features

### Adding a New Section

To add a new section, you need to locate an existing section to replace and include the new section:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md "Usage" '## Usage

This is the updated usage section.

## New Section

This is a completely new section that will be inserted after Usage.

### New Subsection

With nested content.
'
```

### Batch Section Updates

Create a batch file for updating multiple sections:

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "Installation", 
      "code": "## Installation\n\nNew installation instructions.\n"
    },
    {
      "method": "Troubleshooting", 
      "code": "## Troubleshooting\n\nNew troubleshooting guide.\n"
    }
  ]
}
EOF

cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py documentation.md --batch updates.json
```

## Token Efficiency Best Practices

1. **Minimize Inspections**: Inspect the document structure once, then perform all needed operations
2. **Avoid Unnecessary Previews**: Only preview sections when you genuinely need to see current content
3. **Use Batch Operations**: For multiple section updates, use batch files instead of sequential operations
4. **Targeted Updates**: Only replace sections that actually need to change
5. **Preserve Heading Structure**: Keep the same heading level (# vs ##) when replacing sections

## Integration with Other Tools

The Markdown tool works well with other CodeCRISPR tools and MCP operations:

- Use CodeCRISPR for section-level edits
- Use `write_file` for complete document rewrites
- Use `edit_block` for changes that don't align with section boundaries

## Common Use Cases

### Documentation Updates

```bash
# Update the API documentation section
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py API.md "Authentication" '## Authentication

The authentication process has been updated to use OAuth 2.0. Here's how to implement it:

```code
const token = await getOAuthToken();
```

See the [OAuth documentation](https://example.com/oauth) for details.
'
```

### Section Reorganization

```bash
# Move a section by copying content and replacing in new order
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py guide.md "Introduction" '# Introduction

Introduction text remains the same.

## Quick Start

This section used to be at the end, but now it\'s right after the introduction.

1. Install the package
2. Configure settings
3. Run the application
'
```

## Troubleshooting

- **Section Not Found**: Ensure the heading text matches exactly, including case and any special characters
- **Unexpected Section Boundaries**: Check for inconsistent heading levels or unmarked subsections
- **Content Formatting Issues**: Preserve blank lines and indentation in replacement content
- **Batch Update Failures**: Verify JSON syntax and section names in batch files

## Token Savings Example

Consider updating 3 sections in a 1000-line markdown document:

- **Traditional approach**: 3 full file reads + 3 full file writes = 6000 tokens
- **CodeCRISPR approach**: 1 inspection + 3 targeted section updates = ~1500 tokens
- **Savings**: ~75% reduction in token usage

## Markdown Tool Limitations

The Markdown Tool is designed for reliability and efficiency across most well-structured Markdown documents. However, users should be aware of certain inherent limitations based on the nature of the Markdown format and the tool’s lightweight parsing strategy:

- The tool does not attempt to build a full abstract syntax tree of the document, meaning that although it respects structural boundaries created by headings and ignores false headings inside fenced code blocks, it does not analyze deeper semantic relationships such as paragraphs inside blockquotes, nested list hierarchies, or inline elements with special formatting.
- It cannot selectively modify content within a heading-defined section—such as changing a single bullet point or editing one paragraph—without replacing the entire block associated with that heading. This limitation is intrinsic to a system that works at the section level rather than at the fine-grained token level.
- While the tool is now robust against misinterpreting headings that appear within fenced code blocks (e.g., within triple backtick regions), it may still behave unpredictably with documents that use unconventional structures—such as headings embedded in HTML, or documents that omit heading levels or reuse heading names multiple times.

For most documentation tasks—including changelogs, instructional material, API references, and structured project notes—the tool provides a safe and efficient editing model with significant advantages in clarity and token efficiency.

By following these guidelines, you can efficiently edit Markdown documents while minimizing token usage and maintaining document structure integrity.
