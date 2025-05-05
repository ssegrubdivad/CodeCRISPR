# SQL Tool Guide

## Introduction

The SQL Tool in CodeCRISPR allows structured editing of SQL script files by isolating and replacing entire statement blocks like `CREATE`, `INSERT`, `UPDATE`, `DELETE`, and others. This enables precise editing of SQL commands based on their position and type without altering unrelated statements.

## How the SQL Tool Works

The tool detects SQL blocks by:

1. **Command Detection**: Identifying statements by their leading keywords (e.g., `CREATE`, `INSERT`, `SELECT`)
2. **Statement Termination**: Using the terminating semicolon `;` to determine where a block ends
3. **Reference Mapping**: Assigning each statement a unique key based on its type and starting line (e.g., `SELECT_32`)
4. **Targeted Editing**: Allowing specific replacements using that key without needing to reload the entire script

## Basic Usage Workflow

### 1. Inspect the SQL File

To view all SQL blocks:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py schema.sql --inspect
```

Example output:
```
Inspecting 'schema.sql' [sql_tool]:
  CREATE_2: lines 2–10
  INSERT_12: lines 12–15
  SELECT_20: lines 20–25
```

### 2. Preview a Block

```bash
python3 CC/codecrispr.py schema.sql --inspect --preview "INSERT_12"
```

### 3. Replace a Block

```bash
python3 CC/codecrispr.py schema.sql "SELECT_20" 'SELECT * FROM users WHERE active = 1;'
```

## Advanced Usage

### Batch Replacements

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "CREATE_2",
      "code": "CREATE TABLE logs (id INT, event TEXT);"
    },
    {
      "method": "INSERT_12",
      "code": "INSERT INTO logs VALUES (1, 'start');"
    }
  ]
}
EOF

python3 CC/codecrispr.py schema.sql --batch updates.json
```

## Best Practices

- **Include Semicolons**: Each statement must end with `;` to be detected
- **Maintain Formatting**: Use appropriate indentation for readability
- **Use Correct Block Keys**: Refer to blocks using the format `COMMAND_LINENUMBER`

## Common Use Cases

- Replacing `CREATE TABLE` definitions
- Updating `INSERT` values for initial data loads
- Modifying `SELECT` queries used for reporting

## Troubleshooting

- **Block Not Found**: Double-check case and line number in block key
- **Unterminated Statement**: Ensure `;` ends every statement
- **Multiline Statement Confusion**: Avoid breaking statements across inconsistent lines

## Token Efficiency Example

Editing 4 SQL statements in a 500-line file:

- Traditional editing: ~2000 tokens
- SQL Tool editing: ~400 tokens
- **Savings**: ~80%

## Limitations

- Only parses top-level SQL commands
- Does not support embedded procedural code (e.g., PL/pgSQL blocks)
- Ignores commented-out SQL

The SQL Tool is ideal for managing migrations, schema definitions, data seed files, and test scripts.