# Swift Tool Guide

## Introduction

The Swift Tool extends CodeCRISPR's capabilities to support editing Swift source files at the function level. This tool identifies, previews, and replaces Swift `func` declarations, including instance methods and those marked with `override`.

## How the Swift Tool Works

The tool operates by analyzing Swift source code using pattern recognition:

1. **Finds Functions**: Searches for `func` declarations including those with `override`
2. **Tracks Structure**: Uses brace tracking to determine where each function begins and ends
3. **Enables Edits**: Allows users or AI to replace functions by name without needing to reload the full file

## Core Features

- **Function Detection**: Handles methods with and without `override`, return types, and parameters
- **Scope Tracking**: Uses brace counting to safely extract function boundaries
- **Precision Edits**: Replaces only the specified function, preserving file structure
- **Batch and Preview Support**: Fully compatible with CodeCRISPR’s inspect, preview, and batch modes

## Basic Usage Workflow

### 1. Inspect the File

Start by scanning the file structure:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py MyFile.swift --inspect
```

Example output:
```
Inspecting 'MyFile.swift' [swift_tool]:
  viewDidLoad: lines 5–15
  fetchData: lines 17–32
  renderView: lines 34–42
```

### 2. Preview a Function

Preview a function before replacing it:

```bash
python3 CC/codecrispr.py MyFile.swift --inspect --preview "fetchData"
```

### 3. Replace a Function

To update `renderView` with new content:

```bash
python3 CC/codecrispr.py MyFile.swift "renderView" 'func renderView() {
    print("Rendering updated view.")
}'
```

## Advanced Usage

### Supporting `override` and Return Types

The tool matches methods such as:

```swift
override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
    return data.count
}
```

You can refer to this method simply as `tableView` when replacing it.

### Batch Function Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "viewDidLoad",
      "code": "override func viewDidLoad() {\n    super.viewDidLoad()\n    setupUI()\n}"
    },
    {
      "method": "fetchData",
      "code": "func fetchData() {\n    apiService.load()\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py MyFile.swift --batch updates.json
```

## Token Efficiency Tips

- Inspect once per file and operate using memory
- Use exact method names to avoid mismatches
- Combine multiple replacements into batch instructions

## Common Use Cases

### Logic Refactoring

```bash
python3 CC/codecrispr.py App.swift "calculateScore" 'func calculateScore() -> Int {
    return level * multiplier
}'
```

### Simplifying Lifecycle Hooks

```bash
python3 CC/codecrispr.py ViewController.swift "viewWillAppear" 'override func viewWillAppear(_ animated: Bool) {
    super.viewWillAppear(animated)
    refreshData()
}'
```

## Troubleshooting

- **Method Not Found**: Ensure exact spelling and case
- **Unbalanced Braces**: Verify that the replacement code is complete and well-formed
- **Return Type Errors**: Always match the method signature if it includes return values
- **Batch Errors**: Check for missing commas or unescaped newlines in JSON

## Token Efficiency Example

A file with 1200 lines and 4 functions needing updates:

- **Standard approach**: 4 full file loads = ~4800 tokens
- **Swift Tool approach**: 1 inspect + 4 targeted operations = ~1000 tokens
- **Efficiency Gain**: Over 75% savings

## Swift Tool Limitations

- Only supports functions using standard `func` declarations and brace syntax
- Does not support property or computed variable edits
- Assumes well-formed source with matched curly braces

Use this tool to modify Swift code quickly, safely, and with minimal context loading.