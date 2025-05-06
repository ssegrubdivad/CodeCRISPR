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

## Limitations and Edge Cases

### Parsing Limitations

- **Complex Arrow Functions**: Arrow functions with implicit returns or complex destructuring patterns might not be reliably detected.
- **Object Method Shorthand**: Methods defined using shorthand syntax in object literals may be parsed inconsistently.
- **Higher-Order Components**: React HOCs and other function wrappers can confuse the parser when heavily nested.
- **Dynamic Property Names**: Methods using computed property names (e.g., `[dynamicName]() {}`) may not be correctly identified.
- **JSX Boundaries**: The tool might struggle with JSX when it contains functions or methods defined inline.
- **Template Literals**: Functions containing complex template literals with embedded expressions might cause parsing issues.

### Handling Edge Cases

- Convert arrow functions to standard function syntax temporarily for complex edits.
- For object methods, consider editing the entire containing object instead of a single method.
- When working with HOCs or heavily wrapped components, use `--preview` to verify correct function boundaries.
- Extract complex JSX into separate components before editing for more reliable parsing.
- For functions with complex template literals, use the file-based input approach (see example below).

### Example Edge Case: Complex Destructuring

The following might be problematic:

```javascript
const processData = ({ 
  id, 
  user: { 
    name = "Anonymous", 
    settings: { theme = "default" } 
  } = {} 
}) => {
  // Function body
};
```

**Solution**: Temporarily simplify to:

```javascript
const processData = (data) => {
  // Function body
};
```

Make your edits, then restore the complex parameter structure.

### Example Edge Case: Dynamic Property Names

```javascript
const handlers = {
  [`handle${eventType}`]: function() {
    // Handler code
  }
};
```

**Solution**: Use `edit_block` for these cases or edit the entire object.

## General Troubleshooting Recommendations

When encountering parsing issues with the JavaScript tool:

1. **Verify File Format**: Ensure the file uses standard JavaScript formatting and syntax.
2. **Simplify Complex Structures**: Temporarily simplify nested or complex structures before editing.
3. **Use Inspection First**: Always use `--inspect` to verify that the target function is correctly identified.
4. **Preview Before Editing**: Use `--preview` to check the exact content that will be modified.
5. **Consider Alternative Approaches**: For particularly complex cases, consider using `edit_block` or `write_file` instead of function replacement.
6. **File-Based Input**: For complex code with special characters, use the file-based input approach described below.
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

## File-Based Input Approach

When working with complex JavaScript functions containing special characters, template literals, or multi-line formatting, the file-based input approach is strongly recommended:

```bash
# Create a temporary file with the exact function code
cat > new_render_function.js << 'EOF'
const renderTemplate = (data) => {
  // Complex template literals with special characters
  return `
    <div class="container">
      ${data.items.map(item => `
        <div class="item" data-id="${item.id}">
          <h3>${item.name}</h3>
          <p>${item.description}</p>
          ${item.isHighlighted ? `<span class="highlight">⭐</span>` : ""}
        </div>
      `).join("")}
    </div>
  `;
};
EOF

# Use command substitution to pass the content
python3 CC/codecrispr.py app.js renderTemplate "$(cat new_render_function.js)"
```

This approach eliminates the need to escape special characters and preserves exact formatting, making it particularly valuable for React components, template rendering functions, and complex data processing logic.
## Token Efficiency Example

Updating 4 of 50 functions in a 1500-line file:

- **Traditional approach**: 4 complete file scans = 6000 tokens
- **JavaScript Tool**: 1 inspection + 4 focused edits = ~1000 tokens
- **Efficiency gain**: Over 80% saved

## JavaScript Tool Limitations

- Does not handle dynamically generated functions (e.g. `new Function(...)`)
- Functions defined inline inside expressions may be missed
- Function names must be explicitly declared (not anonymous)
- Computed property names are not consistently detected
- Extremely nested HOCs or complex React patterns may cause parsing issues
- Arrow functions with implicit returns (no braces) might be detected inconsistently

This tool enables safe and efficient control over JavaScript editing tasks with support for all major modern styles when properly formatted. For edge cases, remember that CodeCRISPR always offers `edit_block` as a reliable fallback option for precise code manipulation.
## JavaScript Tool Limitations

- Does not handle dynamically generated functions (e.g. `new Function(...)`)
- Functions defined inline inside expressions may be missed
- Function names must be explicitly declared (not anonymous)

This tool enables safe and efficient control over JavaScript editing tasks with support for all major modern styles.
