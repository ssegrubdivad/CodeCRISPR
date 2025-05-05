# CSS Tool Guide

## Introduction

The CSS Tool in CodeCRISPR is designed to allow efficient editing of CSS rulesets. It enables precise targeting of selectors such as classes (`.class`), IDs (`#id`), and element names (`div`, `body`, etc.), and replaces entire declaration blocks. This guide explains how to inspect, preview, and update CSS rules within your stylesheets.

## How the CSS Tool Works

The tool works by parsing CSS files line-by-line using regular expressions that detect the start of a ruleset and then track the opening `{` and closing `}` braces to determine its boundaries.

1. **Selector Detection**: Recognizes standard CSS selectors at the beginning of a block
2. **Brace-Based Scoping**: Tracks the number of opening and closing braces to find the full extent of each block
3. **Block Mapping**: Builds a reference map of all selectors with their line ranges
4. **Block Replacement**: Allows for safe and efficient substitution of entire CSS blocks

## Core Features

- **Selector-Aware Parsing**: Targets blocks by selector name (e.g., `.container`, `#main`, `h1`)
- **Scope-Safe Replacement**: Ensures only the matched block is replaced
- **Whitespace Tolerant**: Flexible enough to handle spaces and formatting differences
- **Minimal Token Usage**: Reads and writes only relevant sections

## Basic Usage Workflow

### 1. Inspect the CSS File

Begin by listing all selectors in the file:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py styles.css --inspect
```

Example output:
```
Inspecting 'styles.css' [css_tool]:
  body: lines 0–5
  .container: lines 7–14
  #main: lines 16–22
  h1: lines 24–28
```

### 2. Preview a Block

To preview the `.container` block:

```bash
python3 CC/codecrispr.py styles.css --inspect --preview ".container"
```

### 3. Replace a Block

To replace the `#main` selector block:

```bash
python3 CC/codecrispr.py styles.css "#main" '#main {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
}'
```

## Advanced Usage

### Recognized Selector Types

- **Class selectors**: `.header`, `.card`
- **ID selectors**: `#footer`, `#nav`
- **Element tags**: `body`, `section`, `p`
- **Simple combinations** (if they start a block): `ul li`, `article > p`

You must reference the selector exactly as defined (including `.` or `#`).

### Batch Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": ".container",
      "code": ".container {\n    margin: 0 auto;\n    max-width: 1200px;\n}"
    },
    {
      "method": "h1",
      "code": "h1 {\n    font-size: 2rem;\n    color: #333;\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py styles.css --batch updates.json
```

## Best Practices

- **Include Full Block**: Always provide full replacement including the selector line and braces
- **Indent Consistently**: For better readability and diffing
- **Preview Before Replace**: Confirm your target block with `--preview`

## Common Use Cases

### Theming or Branding Updates

```bash
python3 CC/codecrispr.py styles.css ".theme-dark" '.theme-dark {
    background-color: #111;
    color: #eee;
}'
```

### Layout Adjustments

```bash
python3 CC/codecrispr.py styles.css ".grid" '.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}'
```

## Troubleshooting

- **Selector Not Found**: Ensure you include the full name, including dot or hash
- **Unbalanced Braces**: Replacement code must be syntactically correct
- **Nested Selectors**: Only the top-level block will be detected and replaced
- **Hidden Declarations**: Ensure your code doesn't include block-openers within comment blocks

## Token Efficiency Example

For 5 updates in a 1000-line stylesheet:

- **Traditional approach**: 5 full-file edits = 5000 lines
- **CSS Tool approach**: 1 inspect + 5 scoped updates = ~600 lines
- **Token savings**: ~88%

## CSS Tool Limitations

- Only replaces complete top-level CSS blocks
- Cannot target nested selectors within media queries or keyframes unless those are top-level selectors
- Does not currently support SCSS nesting or media queries with shared block scope

The CSS Tool provides a fast and accurate way to edit web stylesheets without the need to transmit or tokenize the full file content.