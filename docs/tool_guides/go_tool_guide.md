# Go Tool Guide

## Introduction

The Go Tool extends CodeCRISPR's functionality to support efficient function-level editing of Go source files. This guide explains how to use the tool effectively to identify, preview, and replace Go functions based on their names.

## How the Go Tool Works

Unlike text editors or find-and-replace tools, the Go Tool performs structural parsing of Go code by:

1. **Locating Go Functions**: Scans the source file for function definitions using Go syntax patterns
2. **Mapping Each Function**: Records line numbers for the start and end of each function
3. **Enabling Code Replacement**: Replaces a complete function by name with new source code provided by the user or AI

## Core Features

- **Function Recognition**: Supports regular functions and methods with receivers
- **Brace-Aware Parsing**: Tracks opening and closing braces to determine function boundaries
- **Minimal Token Usage**: Operates on specific line ranges rather than entire files
- **Safe Structural Replacement**: Avoids overlapping or partial code edits

## Basic Usage Workflow

### 1. Inspect the Go Source File

Begin by inspecting the file structure:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py program.go --inspect
```

Sample output:
```
Inspecting 'program.go' [go_tool]:
  Init: lines 5–12
  Run: lines 14–28
  handleEvent: lines 30–45
```

### 2. Preview a Function

To preview the `Run` function:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py program.go --inspect --preview "Run"
```

This shows only the lines corresponding to the `Run` function, helping you review before replacing.

### 3. Replace a Function

To replace the `handleEvent` function:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py program.go "handleEvent" 'func handleEvent(e Event) {
    log.Println("Handling event:", e.Type)
    if e.Type == "click" {
        handleClick(e)
    }
}'
```

The tool replaces only the lines associated with that function.

## Advanced Usage

### Receiver Methods Support

The tool identifies both standard and receiver-based methods:

```go
func (s *Server) handleRequest(req Request) {
    // ...
}
```

You can refer to it simply as `handleRequest` when replacing.

### Batch Updates

Use a batch JSON file for multiple updates:

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "Init", 
      "code": "func Init() {
    fmt.Println(\"Init complete\")
}"
    },
    {
      "method": "Run", 
      "code": "func Run() {
    fmt.Println(\"Running...\")
}"
    }
  ]
}
EOF

cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py program.go --batch updates.json
```

## Best Practices for Token Efficiency

- Run `--inspect` only once per file session
- Use previews before replacements to confirm correct targeting
- Combine changes using `--batch` to minimize instruction overhead
- Always provide well-formed Go function definitions

## Common Use Cases

### Updating Logic in a Function

```bash
python3 CC/codecrispr.py app.go "UpdateDatabase" 'func UpdateDatabase(db *sql.DB) error {
    log.Println("Starting database update")
    return db.Ping()
}'
```

### Refactoring Function Bodies

```bash
python3 CC/codecrispr.py main.go "Run" 'func Run() {
    initialize()
    startWorker()
    waitForShutdown()
}'
```

## Troubleshooting

- **Function Not Found**: Confirm the function name matches exactly and exists in the file
- **Invalid Go Syntax**: Ensure your replacement is syntactically correct
- **Braces Mismatched**: The tool assumes balanced `{}` braces; malformed code may break parsing
- **Batch Errors**: Validate JSON structure and use escaped characters properly

## Token Efficiency Example

For a file with 800 lines and 5 functions to update:

- **Traditional approach**: Read/write entire file 5 times = ~4000 lines processed
- **Go Tool approach**: 1 inspect + 5 targeted updates = ~1000 lines processed
- **Token savings**: ~75% reduction in I/O and memory usage

## Go Tool Limitations

- Only supports top-level and receiver-bound functions with brace-delimited bodies
- Cannot edit comments or inline code outside function definitions
- Functions must have standard brace `{}` enclosures

Use this tool for safe, structural edits to your Go programs and enjoy the precision of method-level control.