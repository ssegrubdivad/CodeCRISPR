# JSON Tool Guide

## Introduction

The JSON Tool in CodeCRISPR provides fine-grained editing of JSON files by allowing the replacement of deeply nested key-value pairs. It supports navigation through both objects and arrays and ensures proper formatting of the modified file.

## How the JSON Tool Works

1. **Key Path Mapping**: Each nested key is mapped using `::` separators (e.g., `settings::theme::dark`)
2. **Targeted Replacement**: Values can be updated individually by specifying the full key path
3. **JSON Integrity**: The tool reads and writes using `json` parsing to ensure correctness

## Basic Usage Workflow

### Inspect the File

```bash
python3 CC/codecrispr.py config.json --inspect
```

Output:
```
Inspecting 'config.json' [json_tool]:
  settings::theme: {...}
  settings::theme::dark: true
  users::0::name: "Alice"
```

### Replace a Value

```bash
python3 CC/codecrispr.py config.json "settings::theme::dark" "false"
```

### Replace an Object

```bash
python3 CC/codecrispr.py config.json "settings::theme" '{ "dark": false, "contrast": "high" }'
```

## Batch Replacement

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "settings::theme::dark",
      "code": "false"
    },
    {
      "method": "users::0::name",
      "code": "\"Bob\""
    }
  ]
}
EOF

python3 CC/codecrispr.py config.json --batch updates.json
```

## Notes

- All values passed to `--code` must be valid JSON (e.g., strings must be quoted)
- Lists are navigated by numeric index: `users::2::email`
- Use `--inspect` to confirm exact key paths before editing

## Limitations

- Does not preserve comments or formatting from original file
- Only replaces individual values or objects, not entire arrays
- String values must be escaped appropriately

This tool is ideal for updating configuration files, user data, application state, and AI prompts in JSON format.