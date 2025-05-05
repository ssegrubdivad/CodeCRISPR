# PHP Tool Guide

## Introduction

The PHP Tool in CodeCRISPR provides precise editing for functions and methods within PHP files. It recognizes regular functions, class methods (with visibility modifiers), magic methods, anonymous functions, and modern arrow functions (PHP 7.4+). This guide explains how to use the tool to inspect, preview, and replace PHP code structures safely and efficiently.

## How the PHP Tool Works

The tool parses PHP source files using regular expressions that detect:

1. **Standard and Static Methods**: `public static function foo(...) { ... }`
2. **Magic Methods**: Like `__construct()` or `__toString()`
3. **Anonymous Functions**: `$action = function(...) { ... };`
4. **Arrow Functions**: `$sum = fn($a, $b) => $a + $b;`
5. **Brace Scoping**: Uses balanced braces to determine function boundaries

It builds a reference map of recognized definitions, enabling targeted replacement without affecting the rest of the file.

## Core Features

- **Multi-Pattern Matching**: Supports visibility modifiers, abstract and final methods
- **Arrow Function Support**: Identifies and replaces modern one-liners
- **Handles Anonymous Closures**: Recognizes `function` assigned to variables
- **Token Efficiency**: Replaces only matched method bodies

## Basic Usage Workflow

### 1. Inspect the PHP File

To view available methods:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py index.php --inspect
```

Sample output:
```
Inspecting 'index.php' [php_tool]:
  __construct: lines 10–18
  getData: lines 20–28
  $handleSubmit: lines 30–34
  $sum: lines 36–36
```

### 2. Preview a Function or Method

To view `getData` before editing:

```bash
python3 CC/codecrispr.py index.php --inspect --preview "getData"
```

### 3. Replace a Function

To update `$sum`:

```bash
python3 CC/codecrispr.py index.php "$sum" '$sum = fn($a, $b) => $a * $b;'
```

Or to update `__construct`:

```bash
python3 CC/codecrispr.py index.php "__construct" 'public function __construct() {
    $this->init();
}'
```

## Advanced Usage

### Abstract and Interface Methods

The tool will recognize:

```php
abstract protected function calculate(): int;
```

Although it cannot be replaced (no body), it can be inspected.

### Anonymous Function Blocks

The tool recognizes:

```php
$logger = function($msg) use ($context) {
    echo "[LOG] $msg";
};
```

It targets `$logger` for replacement.

### Batch Function Replacement

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "getData",
      "code": "public function getData() {\n    return $this->db->fetchAll();\n}"
    },
    {
      "method": "$handleSubmit",
      "code": "$handleSubmit = function($form) {\n    echo \"Submitted\";\n};"
    }
  ]
}
EOF

python3 CC/codecrispr.py index.php --batch updates.json
```

## Best Practices

- **Use Dollar Signs** for variables (e.g., `$logger`) in anonymous/arrow function names
- **Preserve Visibility Modifiers** when replacing class methods
- **Handle Abstract Functions** with care—they cannot be given a body
- **Balance Braces** in function blocks, especially with embedded PHP

## Common Use Cases

### Replacing a Magic Method

```bash
python3 CC/codecrispr.py service.php "__toString" 'public function __toString() {
    return $this->name;
}'
```

### Adjusting Closure Logic

```bash
python3 CC/codecrispr.py handler.php "$onClick" '$onClick = function($event) {
    echo "Clicked!";
};'
```

## Troubleshooting

- **Function Not Found**: Ensure name matches exactly (case-sensitive, include `$` for variables)
- **No Body Found**: May indicate an abstract declaration
- **Unmatched Braces**: All replacement code must be syntactically balanced
- **Line Confusion**: Functions with inline comments may slightly offset pattern matching

## Token Efficiency Example

Editing 5 functions in a 900-line file:

- **Traditional editing**: 5 reads/writes = 4500 lines processed
- **PHP Tool approach**: 1 inspect + 5 edits = ~600 lines handled
- **Savings**: ~85%

## PHP Tool Limitations

- Does not yet support nested anonymous functions or closures inside arrays
- Cannot edit docblock comments directly attached to functions
- Only works on `.php` files with syntactically valid function structures

This tool is ideal for rapid, token-efficient PHP code editing by AIs or developers working in MCP-aware environments.