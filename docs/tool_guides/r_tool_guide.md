# R Tool Guide

## Introduction

The R Tool in CodeCRISPR enables safe and efficient editing of R function definitions. It identifies functions defined using either `<-` or `=` assignment operators and replaces the full function block. This guide outlines how to inspect, preview, and update R code using structured edits.

## How the R Tool Works

The tool uses regular expressions to detect:

1. **Named Functions**: Matches `name <- function(...)` or `name = function(...)`
2. **Brace-Scoped Blocks**: Uses `{}` counting to determine where the function body starts and ends
3. **Function Mapping**: Creates a reference map of all named function blocks

## Core Features

- **Dual Syntax Support**: Handles both `<-` and `=` assignment styles
- **Brace Counting Logic**: Ensures reliable block detection even with nested expressions
- **Name-Based Editing**: Replace functions by referencing their defined names
- **Efficient Modification**: Edits only targeted blocks, preserving the rest of the script

## Basic Usage Workflow

### 1. Inspect the File

View all parsed R functions:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py analysis.R --inspect
```

Example output:
```
Inspecting 'analysis.R' [r_tool]:
  load_data: lines 3–10
  summarize: lines 12–20
  plot_results: lines 22–30
```

### 2. Preview a Function

To preview `summarize`:

```bash
python3 CC/codecrispr.py analysis.R --inspect --preview "summarize"
```

### 3. Replace a Function

To update `plot_results`:

```bash
python3 CC/codecrispr.py analysis.R "plot_results" 'plot_results <- function(data) {
    plot(data$x, data$y, main = "Updated Scatterplot")
}'
```

## Advanced Usage

### Compatible Syntax Styles

The tool supports both:

```r
calculate <- function(x) {
    return(x^2)
}
```

And:

```r
calculate = function(x) {
    return(x^2)
}
```

Both forms are stored as `calculate` in the reference map.

### Batch Replacements

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "load_data",
      "code": "load_data <- function(file) {\n  read.csv(file, stringsAsFactors = FALSE)\n}"
    },
    {
      "method": "summarize",
      "code": "summarize <- function(df) {\n  summary(df)\n}"
    }
  ]
}
EOF

python3 CC/codecrispr.py analysis.R --batch updates.json
```

## Best Practices

- **Use Explicit Names**: Match function names exactly
- **Balanced Braces**: Replacement code must contain correct `{}` pairs
- **Preserve Return Type**: Ensure returned structures match expected usage
- **Comment Carefully**: Inline `{` in comments may confuse parsing

## Common Use Cases

### Editing a Data Processing Function

```bash
python3 CC/codecrispr.py clean.R "clean_data" 'clean_data <- function(df) {
    df <- na.omit(df)
    df <- df[df$age > 18, ]
    return(df)
}'
```

### Adjusting a Plot Generator

```bash
python3 CC/codecrispr.py visuals.R "draw_histogram" 'draw_histogram <- function(vec) {
    hist(vec, col = "skyblue", main = "Histogram")
}'
```

## Troubleshooting

- **Function Not Found**: Ensure the function is defined with a name, and you're using the correct case
- **Brace Mismatch**: Replacement must begin and end with matched `{` and `}`
- **Undetected Functions**: Only functions assigned directly to names are recognized
- **Nested Assignments Ignored**: The tool does not parse functions inside other expressions

## Token Efficiency Example

For 4 updates in an 800-line R script:

- **Traditional method**: Full reads/writes = ~3200 tokens
- **R Tool method**: 1 inspect + 4 updates = ~600 tokens
- **Savings**: ~80%

## R Tool Limitations

- Only detects top-level named functions
- Does not yet parse S3/S4 class methods or closures inside lists
- Comments containing `{` may disrupt brace tracking if not filtered cleanly

The R Tool is a reliable and token-efficient way to manipulate R scripts programmatically, especially within AI-driven or reproducible research workflows.