# SPSS Tool Guide

## Introduction

The SPSS Tool in CodeCRISPR provides reliable, structure-aware editing for SPSS syntax files. It identifies discrete procedure blocks, such as `FREQUENCIES`, `REGRESSION`, `DESCRIPTIVES`, and others, based on command keywords and period-terminated statements. This guide explains how to inspect, preview, and replace individual procedure blocks.

## How the SPSS Tool Works

The parser uses the following logic to identify blocks:

1. **Command Detection**: Matches lines that begin with a valid keyword followed by a terminating period `.` (case-insensitive)
2. **Block Scoping**: Groups contiguous lines until the end of the procedure, marked by a standalone `.`
3. **Reference Mapping**: Each block is uniquely identified by the command and its line number (e.g., `frequencies_12`)
4. **Targeted Replacement**: Replaces only the lines associated with the selected block

## Core Features

- **Command-Aware Parsing**: Recognizes major SPSS procedures
- **Period-Based Block Delimiting**: Tracks until `.` to close a block
- **Unique Block IDs**: Uses `command_startline` format for safe targeting
- **Efficient File Editing**: No need to load or rewrite the entire script

## Basic Usage Workflow

### 1. Inspect the SPSS Syntax File

To list all detected SPSS blocks:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py analysis.sps --inspect
```

Example output:
```
Inspecting 'analysis.sps' [spss_tool]:
  frequencies_10: lines 10–15
  descriptives_17: lines 17–20
  regression_22: lines 22–32
```

### 2. Preview a Block

To review `descriptives_17`:

```bash
python3 CC/codecrispr.py analysis.sps --inspect --preview "descriptives_17"
```

### 3. Replace a Block

Update the `frequencies_10` block:

```bash
python3 CC/codecrispr.py analysis.sps "frequencies_10" 'FREQUENCIES VARIABLES=gender agegroup
  /FORMAT=DFREQ
  /ORDER=ANALYSIS
.'
```

## Advanced Usage

### Block Naming Convention

Each procedure is stored under a unique name based on:

```
<command keyword>_<line number of start>
```

For example:

```text
regression_45
```

This allows multiple instances of the same command in a file to be uniquely addressable.

### Batch Block Replacement

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "frequencies_10",
      "code": "FREQUENCIES VARIABLES=gender.\n"
    },
    {
      "method": "regression_22",
      "code": "REGRESSION VARIABLES=income age education.\n"
    }
  ]
}
EOF

python3 CC/codecrispr.py analysis.sps --batch updates.json
```

## Best Practices

- **Always End with a Period**: Each procedure block must end in `.`
- **Use Lowercase Identifiers**: Block IDs are stored in lowercase for consistency
- **Do Not Edit Line Numbers**: If you edit the file externally, re-inspect before modifying again
- **Minimal Whitespace Assumptions**: Avoid placing periods on lines with unrelated content

## Common Use Cases

### Updating Descriptive Statistics

```bash
python3 CC/codecrispr.py analysis.sps "descriptives_17" 'DESCRIPTIVES VARIABLES=score1 score2 score3
  /STATISTICS=MEAN STDDEV MIN MAX
.'
```

### Adjusting a Regression Block

```bash
python3 CC/codecrispr.py analysis.sps "regression_22" 'REGRESSION
  /DEPENDENT y
  /METHOD=ENTER x1 x2 x3
.'
```

## Troubleshooting

- **Block Not Found**: Check that the name includes the correct command and line number
- **Unterminated Procedure**: Ensure every SPSS procedure ends with `.`
- **Unexpected End Behavior**: Avoid mixing commands on the same line as `.`
- **Unparsed Commands**: Only procedures with clearly marked periods will be detected

## Token Efficiency Example

For 4 procedure replacements in a 600-line SPSS file:

- **Traditional rewriting**: ~2400 tokens
- **SPSS Tool approach**: ~500 tokens
- **Efficiency gain**: ~79%

## SPSS Tool Limitations

- Only detects procedure blocks that start with a word and end with `.`
- Comments, macros, or inline conditional blocks are not interpreted
- Multiline continuation blocks (`+`, `~`) must still end with `.`
- Embedded scripting logic (e.g., Python blocks) is not parsed

The SPSS Tool is optimized for common statistical workflows, allowing AI or users to surgically adjust analyses while avoiding the cost of full-context editing.