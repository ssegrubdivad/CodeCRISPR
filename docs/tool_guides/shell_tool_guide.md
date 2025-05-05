# Shell Tool Guide

## Introduction

The Shell Tool for CodeCRISPR enables isolated editing of Bash and POSIX shell functions within `.sh` or `.bash` scripts. It recognizes standard shell function definitions and allows for modular updates without reloading or rewriting the entire script.

## How the Shell Tool Works

1. **Function Identification**: Matches patterns like `myfunc() {` at the start of lines
2. **Brace Matching**: Tracks nested braces to determine function block boundaries
3. **Function Mapping**: Tags each block using the function name (e.g., `backup`)
4. **Token Efficiency**: Operates on only the target block rather than the whole file

## Usage

### 1. Inspect the Script

```bash
python3 CC/codecrispr.py backup.sh --inspect
```

Sample Output:
```
Inspecting 'backup.sh' [shell_tool]:
  backup: lines 5–15
  compress: lines 17–24
```

### 2. Preview a Block

```bash
python3 CC/codecrispr.py backup.sh --inspect --preview "backup"
```

### 3. Replace a Function

```bash
python3 CC/codecrispr.py backup.sh "compress" 'compress() {
  tar -czf $1.tar.gz $1
}'
```

## Batch Update

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "backup",
      "code": "backup() {\n  echo \"Backing up...\"\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py backup.sh --batch updates.json
```

## Notes

- Recognizes only traditional shell functions: `name() { ... }`
- Inline or anonymous functions are not supported
- Handles nested braces with basic counting (not strings/comments)

## Use Cases

- Replacing build, deploy, backup, or utility shell functions
- Maintaining cron jobs, setup scripts, and toolchains

## Limitations

- Does not evaluate shell quoting/escaping
- Brace misalignment (e.g., inside strings) may cause block parsing errors
- Ignores functions without matching `{}` bodies

This tool provides a robust way to modularly maintain shell scripts and automate edits with AI support.