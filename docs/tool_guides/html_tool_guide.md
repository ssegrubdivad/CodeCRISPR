# HTML Tool Guide

## Introduction

The HTML Tool in CodeCRISPR allows for safe and efficient editing of `<div>` blocks within HTML documents, specifically those marked with unique `id` attributes. It identifies and replaces entire `div` sections using structural tag-matching, ideal for templated or modular HTML editing.

## How the HTML Tool Works

This tool scans an HTML file line-by-line for `<div>` elements with `id="..."`, then uses nesting depth to determine the full extent of each block:

1. **Block Identification**: Detects `<div id="...">` tags
2. **Depth Tracking**: Follows nested `<div>` elements using a counter
3. **End Detection**: Identifies the matching closing `</div>` tag
4. **Map Construction**: Builds a reference of named blocks and their line ranges
5. **Block Replacement**: Enables safe substitution of the matched `div` section

## Core Features

- **`id`-Based Targeting**: Operates on blocks with unique identifiers
- **Nesting Awareness**: Handles multiple nested `<div>` layers
- **Strict Tag Matching**: Preserves valid HTML structure during replacement
- **Efficient Token Use**: Only modifies required blocks

## Basic Usage Workflow

### 1. Inspect the HTML File

To view replaceable `<div id="...">` blocks:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py page.html --inspect
```

Example output:
```
Inspecting 'page.html' [html_tool]:
  header: lines 3–12
  content: lines 14–35
  footer: lines 37–45
```

### 2. Preview a Block

To see the `content` block before editing:

```bash
python3 CC/codecrispr.py page.html --inspect --preview "content"
```

### 3. Replace a Block

Replace the `footer` section:

```bash
python3 CC/codecrispr.py page.html "footer" '<div id="footer">
    <p>&copy; 2025 My Website</p>
</div>'
```

## Advanced Usage

### Handling Nested `div`s

The tool tracks nesting depth, so this structure is handled correctly:

```html
<div id="sidebar">
    <div class="widget">...</div>
    <div class="widget">...</div>
</div>
```

When you replace `sidebar`, the entire nested content is replaced in one operation.

### Batch Block Replacement

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "header",
      "code": "<div id=\"header\">\n  <h1>Welcome!</h1>\n</div>"
    },
    {
      "method": "content",
      "code": "<div id=\"content\">\n  <p>Updated content here.</p>\n</div>"
    }
  ]
}
EOF

python3 CC/codecrispr.py page.html --batch updates.json
```

## Best Practices

- **Include Full Block**: Always supply full opening and closing tags when replacing
- **Preserve Formatting**: Match indentation and line breaks for readability
- **Avoid Duplicate IDs**: Ensure each `id` is unique per HTML spec
- **Escape Quotes in JSON**: Use `\"` in JSON batch files for attribute values

## Common Use Cases

### Replacing a Section

```bash
python3 CC/codecrispr.py home.html "intro" '<div id="intro">
    <h2>About Us</h2>
    <p>We build tools for the future.</p>
</div>'
```

### Swapping Modular Components

```bash
python3 CC/codecrispr.py layout.html "nav" '<div id="nav">
    <ul><li>Home</li><li>Docs</li></ul>
</div>'
```

## Troubleshooting

- **Block Not Found**: Ensure `id` matches exactly (case-sensitive)
- **Invalid Nesting**: Mismatched tags may cause incorrect depth calculation
- **Incomplete Replacements**: Always include both `<div>` and `</div>` when replacing
- **Duplicate IDs**: Only the first matching block will be used

## Token Efficiency Example

Editing 3 blocks in a 1500-line HTML file:

- **Traditional editing**: 3 full loads = ~4500 tokens
- **HTML Tool method**: 1 inspect + 3 replacements = ~700 tokens
- **Token savings**: ~84%

## HTML Tool Limitations

- Only supports blocks with `id="..."` on `<div>` tags
- Does not yet support other tags (like `section`, `nav`, etc.)
- Assumes well-formed and indented HTML for best results
- JavaScript-rendered DOM content is not detected

This tool is ideal for managing modular HTML documents, CMS templates, and static site editing workflows efficiently with minimal context requirements.