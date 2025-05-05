# C++ Tool Guide

## Introduction

The C++ Tool in CodeCRISPR enables function- and method-level editing of C++ source code. It supports parsing of free functions, class methods, constructors, destructors, and template-based declarations. This guide explains how to locate, preview, and replace C++ method definitions using the tool.

## How the C++ Tool Works

The tool scans C++ files using multiple regular expressions designed to match:

1. **Class Methods**: Including `ClassName::methodName(...) { ... }`
2. **Free Functions**: Such as `int add(int a, int b) { ... }`
3. **Constructors/Destructors**: Including `MyClass(...) { ... }` and `~MyClass() { ... }`
4. **Template Functions**: Recognizes template headers and body pairs
5. **Brace Counting**: Uses `{}` to determine the start and end of functions, ignoring comments and string literals

## Core Features

- **Multi-Form Parsing**: Recognizes inline, static, constexpr, and template functions
- **Preprocessor-Aware**: Skips over `#include`, `#define`, and other directives
- **Brace Scope Counting**: Safely tracks function block boundaries
- **Constructor/Destructor Support**: Detects and replaces class lifecycle methods

## Basic Usage Workflow

### 1. Inspect the File

List all recognized C++ methods and functions:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py module.cpp --inspect
```

Example output:
```
Inspecting 'module.cpp' [cpp_tool]:
  Math::add: lines 10–18
  MyClass::MyClass: lines 20–25
  ~MyClass: lines 27–30
  computeAverage: lines 32–40
```

### 2. Preview a Method

To preview `computeAverage`:

```bash
python3 CC/codecrispr.py module.cpp --inspect --preview "computeAverage"
```

### 3. Replace a Method

To update `Math::add`:

```bash
python3 CC/codecrispr.py module.cpp "Math::add" 'int Math::add(int a, int b) {
    return a + b + 1; // adjusted addition
}'
```

## Advanced Usage

### Supporting Templates and Qualifiers

The tool recognizes function signatures like:

```cpp
template <typename T>
inline T max(const T& a, const T& b) {
    return (a > b) ? a : b;
}
```

Or:

```cpp
MyClass::~MyClass() noexcept {
    // cleanup logic
}
```

### Batch Replacements

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "computeAverage",
      "code": "double computeAverage(std::vector<int>& v) {\n  return std::accumulate(v.begin(), v.end(), 0.0) / v.size();\n}"
    },
    {
      "method": "MyClass::MyClass",
      "code": "MyClass::MyClass() {\n  init();\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py module.cpp --batch updates.json
```

## Best Practices

- **Use Fully Qualified Names**: For class methods, use `ClassName::methodName`
- **Match Constructor Names**: Exactly as declared in the class
- **Preserve Return Types**: Especially for templates or overloaded functions
- **Bracket Balance**: Replacement must include matching `{}`

## Common Use Cases

### Refactoring a Class Method

```bash
python3 CC/codecrispr.py model.cpp "MyClass::train" 'void MyClass::train() {
    // New training logic here
}'
```

### Updating Global Utility Functions

```bash
python3 CC/codecrispr.py utils.cpp "clamp" 'int clamp(int value, int min, int max) {
    return std::max(min, std::min(max, value));
}'
```

## Troubleshooting

- **Function Not Found**: Double-check for fully qualified names or typographical errors
- **Unclosed Braces**: Ensure that all replacements have balanced `{}` blocks
- **Inline Comments or Macros**: May interfere with detection if improperly closed
- **Templates Across Lines**: Only works when template declaration and function header are contiguous

## Token Efficiency Example

Editing 4 methods in a 2000-line `.cpp` file:

- **Traditional method**: 4 full reads/writes = ~8000 tokens
- **C++ Tool method**: 1 inspect + 4 replacements = ~1100 tokens
- **Savings**: Over 85%

## C++ Tool Limitations

- Does not currently parse header files (`.h`) separately unless they contain inline definitions
- Does not reconstruct or modify declaration prototypes—only the implementation blocks
- Multi-line macros or deeply nested lambdas inside functions may be misinterpreted

This tool provides a fast, safe, and structured way to manipulate C++ code blocks, especially useful in automated or AI-assisted development workflows.