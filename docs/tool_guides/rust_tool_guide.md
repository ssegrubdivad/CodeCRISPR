# Rust Tool Guide

## Introduction

The Rust Tool in CodeCRISPR allows precise editing of functions and methods within Rust source files. It supports free-standing functions, trait implementations, and methods defined in `impl` blocks. This guide explains how to locate, preview, and replace Rust functions safely and efficiently.

## How the Rust Tool Works

The tool identifies functions by parsing for:

1. **Free Functions**: `fn main() { ... }`
2. **Methods in `impl` Blocks**: `impl Type { fn new(...) { ... } }`
3. **Function Modifiers**: Including `pub`, `async`, `const`, and `unsafe`
4. **Brace Counting**: Tracks `{}` to determine the boundaries of each function

During parsing, it also tracks whether a function appears inside an `impl` block, so the function can be mapped using the qualified name `Type::method`.

## Core Features

- **Function & Method Matching**: Recognizes both standalone and associated functions
- **Impl Block Support**: Understands method ownership by type
- **Brace Scope Detection**: Counts braces to ensure correct block parsing
- **Supports Common Modifiers**: Handles `pub`, `async`, `const`, `unsafe`, and generic parameters

## Basic Usage Workflow

### 1. Inspect the Rust File

List all detected functions and methods:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py main.rs --inspect
```

Example output:
```
Inspecting 'main.rs' [rust_tool]:
  main: lines 2–10
  Config::new: lines 12–20
  Config::load: lines 22–35
```

### 2. Preview a Function

To view `Config::new`:

```bash
python3 CC/codecrispr.py main.rs --inspect --preview "Config::new"
```

### 3. Replace a Function

Replace `Config::load`:

```bash
python3 CC/codecrispr.py main.rs "Config::load" 'impl Config {
    pub fn load(path: &str) -> Self {
        println!("Loading config from {}", path);
        Self { path: path.to_string() }
    }
}'
```

## Advanced Usage

### Free and Associated Functions

Free function example:

```rust
pub fn greet() {
    println!("Hello, world!");
}
```

Impl method example:

```rust
impl App {
    pub async fn start(&self) {
        // async startup logic
    }
}
```

Both are matched and stored with or without type prefixes.

### Batch Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "main",
      "code": "fn main() {\n    println!(\"App started\");\n}"
    },
    {
      "method": "Config::new",
      "code": "impl Config {\n    pub fn new() -> Self {\n        Self {}\n    }\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py main.rs --batch updates.json
```

## Best Practices

- **Use Qualified Names**: For methods, always specify `Type::method`
- **Preserve Modifiers**: Include `pub`, `async`, or `unsafe` as needed
- **Brace Integrity**: Ensure `{}` are balanced in replacements
- **Respect Ownership**: Verify updated signatures maintain lifetimes and borrow semantics

## Common Use Cases

### Refactor a Method

```bash
python3 CC/codecrispr.py config.rs "Settings::parse" 'impl Settings {
    pub fn parse(path: &str) -> Result<Self, Error> {
        let content = std::fs::read_to_string(path)?;
        Ok(serde_json::from_str(&content)?)
    }
}'
```

### Update an Async Function

```bash
python3 CC/codecrispr.py server.rs "Server::run" 'impl Server {
    pub async fn run(&self) {
        self.listen().await;
    }
}'
```

## Troubleshooting

- **Function Not Found**: Double-check type name and method (case-sensitive)
- **Unclosed Braces**: All function blocks must have matching braces
- **Ambiguous Matching**: Avoid methods with identical names across multiple impl blocks
- **Traits Not Parsed**: Tool does not yet detect trait declarations or headers

## Token Efficiency Example

Updating 3 functions in a 1000-line file:

- **Traditional approach**: Full read/write = ~3000 tokens
- **Rust Tool approach**: 1 inspect + 3 partial writes = ~600 tokens
- **Savings**: ~80%

## Rust Tool Limitations

- Does not parse trait headers or declarations (only impl blocks with bodies)
- Cannot edit inline macros or procedural macro-generated functions
- Expects properly formatted Rust code (no unmatched or commented-out braces)

This tool is ideal for automated and AI-assisted editing of Rust programs, supporting real-world module structures and syntax while remaining lightweight and context-aware.