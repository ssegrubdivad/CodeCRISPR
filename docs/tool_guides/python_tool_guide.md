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
- **Indentation-Based Parsing**: Honors Python’s whitespace structure for accurate block detection
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

## Token Efficiency Example

Updating 5 out of 100 functions:

- **Full rewrites**: 5 x 500 lines = 2500 lines handled
- **Python Tool**: 1 inspection + 5 updates = ~600 lines
- **Token savings**: ~75%

## Python Tool Limitations

- Only detects top-level and class-level functions using standard Python syntax
- Does not detect nested functions within other functions
- Requires consistent indentation and valid decorators

With the Python Tool, you gain control over function-level editing for AI workflows, scripting tasks, and code generation scenarios with precision and token economy.