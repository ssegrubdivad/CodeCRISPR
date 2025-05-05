# MATLAB Tool Guide

## Introduction

The MATLAB Tool in CodeCRISPR enables accurate and efficient editing of MATLAB `.m` function files. It identifies full function blocks using `function` and `end` keywords and enables safe replacement without affecting unrelated code. This guide explains how to inspect, preview, and replace MATLAB function definitions.

## How the MATLAB Tool Works

The tool parses MATLAB files using:

1. **Function Header Detection**: Recognizes both `[out] = name(...)` and `name(...)` signatures
2. **End Boundary Matching**: Locates the corresponding `end` keyword to identify function extent
3. **Reference Mapping**: Associates function names with start and end line numbers
4. **Safe Replacement**: Substitutes function blocks using name-based targeting

## Core Features

- **Header Style Flexibility**: Supports multiple return/output styles
- **Explicit Block Ends**: Uses `end` for precise boundaries
- **Function Name Indexing**: Replaces functions by name reference
- **Preserves External Code**: Only replaces matched blocks

## Basic Usage Workflow

### 1. Inspect a MATLAB File

Display all detected function blocks:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py process.m --inspect
```

Example output:
```
Inspecting 'process.m' [matlab_tool]:
  normalize: lines 3–12
  transform: lines 14–24
  analyze: lines 26–40
```

### 2. Preview a Function

To view the `transform` block:

```bash
python3 CC/codecrispr.py process.m --inspect --preview "transform"
```

### 3. Replace a Function

Update the `normalize` block:

```bash
python3 CC/codecrispr.py process.m "normalize" 'function y = normalize(x)
    y = (x - mean(x)) / std(x);
end'
```

## Advanced Usage

### Recognized Header Forms

Supported patterns include:

```matlab
function result = myFunction(x)
```

```matlab
function [a, b] = myFunction(x, y)
```

### Batch Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "transform",
      "code": "function y = transform(x)\n    y = x .^ 2;\nend"
    },
    {
      "method": "analyze",
      "code": "function result = analyze(data)\n    result = sum(data);\nend"
    }
  ]
}
EOF

python3 CC/codecrispr.py process.m --batch updates.json
```

## Best Practices

- **Include `end`**: Always close replacement blocks with `end`
- **Use Exact Names**: Target functions by their declared name
- **Preserve Output Format**: Match `[]` if used in original declaration
- **Avoid Inline `end` Confusion**: Ensure `end` appears on its own line for clarity

## Common Use Cases

### Updating a Statistical Function

```bash
python3 CC/codecrispr.py stats.m "computeMean" 'function m = computeMean(x)
    m = sum(x) / length(x);
end'
```

### Changing a Signal Processing Function

```bash
python3 CC/codecrispr.py signal.m "filterSignal" 'function y = filterSignal(x)
    y = medfilt1(x);
end'
```

## Troubleshooting

- **Function Not Found**: Ensure the name is exactly as declared
- **Missing `end`**: Function must end with an `end` line
- **Ambiguous Matches**: Avoid having multiple functions with the same name
- **Multiline Headers**: Functions split across lines may not be detected

## Token Efficiency Example

Updating 3 functions in a 1000-line MATLAB file:

- **Traditional editing**: Full file load/save = ~3000 tokens
- **MATLAB Tool**: 1 inspect + 3 updates = ~500 tokens
- **Savings**: ~83%

## MATLAB Tool Limitations

- Only supports top-level functions (not nested or local functions inside functions)
- Does not yet parse class methods or scripts with function sections
- Multiline or commented-out function declarations may not be detected

The MATLAB Tool is ideal for use in numerical and research computing environments where modular `.m` files are edited frequently by humans or AI systems.