# JavaScript Tool Guide

## Introduction

The JavaScript Tool in CodeCRISPR enables precise editing of JavaScript files at the function level. It supports modern and legacy function styles, including arrow functions, async functions, class methods, and object properties. This guide explains how to inspect, preview, and replace JavaScript function definitions efficiently.

## How the JavaScript Tool Works

The tool parses JavaScript source files by using a set of regular expressions that detect a wide range of function declaration patterns, including:

1. **Named Functions**: `function name(...) { ... }`
2. **Arrow Functions**: `const name = (...) => { ... }`
3. **Class Methods**: `class X { name(...) { ... } }`
4. **Async Functions**: All of the above with `async` keyword
5. **Object Property Functions**: `prop: function(...) { ... }` and `prop: (...) => { ... }`

Brace counting is used to ensure function boundaries are accurately captured even in nested scopes.

## Core Features

- **Multi-Style Matching**: Works with traditional, arrow, and class-bound functions
- **Async and Static Awareness**: Parses modern function syntax with support for `async` and `static`
- **Object Methods Support**: Recognizes functions inside object literals
- **Brace Tracking**: Ensures correct block scope parsing using `{}` balance

## Basic Usage Workflow

### 1. Inspect the File

Begin by listing all recognized functions:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py app.js --inspect
```

Example output:
```
Inspecting 'app.js' [javascript_tool]:
  initApp: lines 2–10
  fetchData: lines 12–25
  renderComponent: lines 27–35
  onClick: lines 37–42
```

### 2. Preview a Function

To view `fetchData` before modifying:

```bash
python3 CC/codecrispr.py app.js --inspect --preview "fetchData"
```

### 3. Replace a Function

Replace the contents of `onClick`:

```bash
python3 CC/codecrispr.py app.js "onClick" 'const onClick = (e) => {
    console.log("New click handler");
    e.preventDefault();
}'
```

## Advanced Usage

### Class Methods and Constructors

Handles class syntax such as:

```js
class View {
    constructor() { ... }

    render() { ... }

    async update() { ... }
}
```

Each method including `constructor` can be targeted for replacement.

### Object Property Functions

Supports both formats:

```js
const utils = {
    formatDate: function(date) { ... },
    clean: (str) => { ... }
};
```

Both `formatDate` and `clean` are addressable.

### Batch Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "initApp",
      "code": "function initApp() {\n  console.log('App initialized');\n}"
    },
    {
      "method": "fetchData",
      "code": "const fetchData = async () => {\n  return await fetch('/api/data');\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py app.js --batch updates.json
```

## Best Practices

- **Use Exact Function Names**: Including constructor where applicable
- **Preserve Async/Arrow Style**: Use matching syntax when replacing
- **Bracket Balance**: Ensure new code has matching braces to avoid breaking structure
- **Preview Before Replace**: Use `--preview` to validate what will be overwritten

## Common Use Cases

### Rewriting Event Handlers

```bash
python3 CC/codecrispr.py ui.js "onSubmit" 'const onSubmit = (form) => {
    alert("Submitted!");
}'
```

### Modifying Service Calls

```bash
python3 CC/codecrispr.py api.js "loadUser" 'async function loadUser() {
    const res = await fetch("/user");
    return await res.json();
}'
```

## Troubleshooting

- **Function Not Found**: Confirm naming matches declaration form
- **Arrow Syntax Confusion**: Ensure parentheses and braces are formatted correctly
- **Unbalanced Braces**: Replacement must be properly enclosed
- **Unsupported Patterns**: Some shorthand or inline one-liners may not be recognized

## Token Efficiency Example

Updating 4 of 50 functions in a 1500-line file:

- **Traditional approach**: 4 complete file scans = 6000 tokens
- **JavaScript Tool**: 1 inspection + 4 focused edits = ~1000 tokens
- **Efficiency gain**: Over 80% saved

## JavaScript Tool Limitations

- Does not handle dynamically generated functions (e.g. `new Function(...)`)
- Functions defined inline inside expressions may be missed
- Function names must be explicitly declared (not anonymous)

This tool enables safe and efficient control over JavaScript editing tasks with support for all major modern styles.