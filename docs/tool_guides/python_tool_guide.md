# Python Tool Guide

## Introduction

The Python Tool within CodeCRISPR provides precision editing of Python source files at the function and method level. It supports both standalone functions and class methods, including decorated and asynchronous functions. This guide explains how to inspect, preview, and replace Python code blocks efficiently.

## How the Python Tool Works

The tool parses Python code by analyzing structural elements such as `def`, `async def`, and decorators. It identifies:

1. **Function Definitions**: Matches both top-level and nested functions
2. **Method Definitions**: Detects class methods, including decorated ones
3. **Decorator Context**: Includes decorators when capturing function blocks
4. **Block Boundaries**: Uses indentation rules to determine where functions end

## Core Features

- **Decorator Awareness**: Captures `@staticmethod`, `@classmethod`, `@property`, and custom decorators
- **Indentation-Based Parsing**: Honors Python's whitespace structure for accurate block detection
- **Async Function Support**: Recognizes both `def` and `async def` signatures
- **Class Context Recognition**: Understands method nesting within class definitions

## Basic Usage Workflow

### 1. Inspect the File

To view all functions and methods:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py script.py --inspect
```

Example output:
```
Inspecting 'script.py' [python_tool]:
  fetch_data: lines 3–12
  save_results: lines 14–22
  Model.__init__: lines 25–30
  Model.train: lines 32–50
```

### 2. Preview a Function

To see the `train` method:

```bash
python3 CC/codecrispr.py script.py --inspect --preview "train"
```

### 3. Replace a Function

To update `save_results`:

```bash
python3 CC/codecrispr.py script.py "save_results" 'def save_results(data, filename):
    with open(filename, "w") as f:
        f.write(data)
'
```

## Limitations and Edge Cases

### Parsing Limitations

- **Decorators**: While the Python tool correctly identifies functions with decorators, it may struggle with complex nested decorators or decorators with multiline arguments.
- **Nested Functions**: Deeply nested functions might not be correctly identified if they have unusual indentation patterns.
- **Conditional Function Definitions**: Functions defined inside conditional blocks (if/else statements) may not be consistently detected.
- **Generated Functions**: Functions created via metaprogramming or `exec()` will not be detected as they exist only at runtime.
- **Async Complexity**: Very complex async functions with nested coroutines might have boundary detection issues.
- **Comments and Docstrings**: Large docstrings or comments within function definitions might occasionally interfere with boundary detection.

### Handling Edge Cases

- For complex decorators, consider temporarily simplifying them before editing.
- For nested functions, edit the parent function instead of trying to target the nested function directly.
- When working with conditional function definitions, edit the entire conditional block using `edit_block` instead.
- Break down complex async functions into smaller, more manageable pieces for more reliable editing.
- If a function contains extensive docstrings or comments that cause parsing issues, temporarily simplify them.

### Example Edge Case: Complex Decorators

The following might be problematic:

```python
@complex_decorator(
    param1="value",
    param2=lambda x: x * 2,
    param3={
        "nested": "structure"
    }
)
def problematic_function():
    pass
```

**Solution**: Edit the entire function including decorators or temporarily simplify to:

```python
@complex_decorator()
def problematic_function():
    pass
```

Make your edits, then restore the decorator complexity.

### Example Edge Case: Conditionally Defined Functions

```python
if CONDITION:
    def conditional_function():
        pass
else:
    def conditional_function():
        pass
```

**Solution**: Use `edit_block` instead of method replacement:

```bash
python3 CC/codecrispr.py script.py edit_block 'if CONDITION:
    def conditional_function():
        pass
else:
    def conditional_function():
        pass' 'if CONDITION:
    def conditional_function():
        # Updated implementation
        pass
else:
    def conditional_function():
        # Updated implementation
        pass'
```

## General Troubleshooting Recommendations

When encountering parsing issues with the Python tool:

1. **Verify File Format**: Ensure the file uses standard Python formatting and syntax.
2. **Simplify Complex Structures**: Temporarily simplify nested or complex structures before editing.
3. **Use Inspection First**: Always use `--inspect` to verify that the target function is correctly identified.
4. **Preview Before Editing**: Use `--preview` to check the exact content that will be modified.
5. **Consider Alternative Approaches**: For particularly complex cases, consider using `edit_block` or `write_file` instead of function replacement.
6. **File-Based Input**: For complex code with special characters, use the file-based input approach as described in the main documentation.

## Advanced Features

### Editing Decorated Methods

This method:

```python
@staticmethod
def load():
    return "loaded"
```

Will be recognized as `load`, and replacement preserves the decorator.

### Replacing Async Functions

The tool supports:

```python
async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        ...
```

Refer to the method as `fetch_async`.

### Batch Replacements

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "fetch_data",
      "code": "def fetch_data():\n    return {}"
    },
    {
      "method": "train",
      "code": "def train():\n    print(\"Training started\")"
    }
  ]
}
EOF

python3 CC/codecrispr.py script.py --batch updates.json
```

## Best Practices

- **Inspect Once**: Cache the structure to reduce redundant parsing
- **Use Exact Names**: Match method names precisely, including case
- **Maintain Indentation**: Ensure consistent indentation in new code
- **Use Async Cautiously**: Replacement must preserve `async` if originally declared
- **Handle Special Characters**: For complex strings or special characters, use the file-based input approach:

```bash
# Create a temporary file with the exact function code
cat > new_function.py << 'EOF'
def process_string(text):
    """Process a string with special characters.
    
    Examples:
        >>> process_string("Hello, world!")
        'HELLO, WORLD!'
    """
    return text.upper()
EOF

# Use command substitution to pass the content
python3 CC/codecrispr.py script.py process_string "$(cat new_function.py)"
```

## Common Use Cases

### Refactoring a Utility Function

```bash
python3 CC/codecrispr.py utils.py "format_date" 'def format_date(dt):
    return dt.strftime("%Y-%m-%d")'
```

### Updating Class Method Logic

```bash
python3 CC/codecrispr.py model.py "train" 'def train(self):
    print("Training...")
    self.fit()'
```

## Troubleshooting

- **Function Not Found**: Confirm the function exists and spelling matches
- **Missing Decorators**: Use `--preview` to confirm what will be replaced
- **Improper Indentation**: Replacement code must be properly indented
- **Token Bloat**: Avoid replacing functions that do not need modification
- **Parser Confusion**: If the parser fails to correctly identify a function, use `edit_block` as a fallback

## Token Efficiency Example

Updating 5 out of 100 functions:

- **Full rewrites**: 5 x 500 lines = 2500 lines handled
- **Python Tool**: 1 inspection + 5 updates = ~600 lines
- **Token savings**: ~75%

With the Python Tool, you gain control over function-level editing for AI workflows, scripting tasks, and code generation scenarios with precision and token economy.
