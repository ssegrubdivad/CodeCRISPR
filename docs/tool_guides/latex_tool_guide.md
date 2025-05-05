# LaTeX Tool Guide

## Introduction

The LaTeX Tool in CodeCRISPR allows you to edit LaTeX documents by targeting specific environments like `table`, `figure`, `equation`, `itemize`, and others. It detects blocks beginning with `\begin{...}` and ending with `\end{...}`, enabling structured replacements of LaTeX content. This guide describes how to inspect, preview, and replace LaTeX environments safely and efficiently.

## How the LaTeX Tool Works

The tool parses LaTeX documents using:

1. **Environment Start Detection**: Matches lines starting with `\begin{environment}`
2. **Environment Closure**: Finds the matching `\end{environment}`
3. **Block Identification**: Constructs a map of block types and their line ranges
4. **Block Keys**: Uses `environment_startline` as a unique identifier for each environment block

## Core Features

- **Environment Recognition**: Handles standard LaTeX environments
- **Block Isolation**: Matches `begin`/`end` pairs to ensure proper scope
- **Unique IDs**: Associates blocks with a clear, consistent key
- **Efficient Editing**: Minimizes tokens by editing only what is necessary

## Basic Usage Workflow

### 1. Inspect the LaTeX Document

List all detected environments:

```bash
cd /Users/$USER/path/to/your/mcp/directory && python3 CC/codecrispr.py paper.tex --inspect
```

Example output:
```
Inspecting 'paper.tex' [latex_tool]:
  abstract_3: lines 3–8
  figure_10: lines 10–18
  equation_20: lines 20–24
```

### 2. Preview an Environment

Preview the `figure_10` block:

```bash
python3 CC/codecrispr.py paper.tex --inspect --preview "figure_10"
```

### 3. Replace an Environment

To update `equation_20`:

```bash
python3 CC/codecrispr.py paper.tex "equation_20" '\begin{equation}
    E = mc^2
\end{equation}'
```

## Advanced Usage

### Supported Environments

This tool works with any environment written using:

```latex
\begin{environment}
...
\end{environment}
```

Including but not limited to:

- `table`
- `figure`
- `equation`
- `align`
- `itemize`
- `enumerate`
- `abstract`

### Batch Environment Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "abstract_3",
      "code": "\\begin{abstract}\nThis paper explores token-efficient tooling.\\end{abstract}"
    },
    {
      "method": "itemize_45",
      "code": "\\begin{itemize}\n\\item Efficient\\n\\item Lightweight\\n\\end{itemize}"
    }
  ]
}
EOF

python3 CC/codecrispr.py paper.tex --batch updates.json
```

## Best Practices

- **Escape Backslashes in JSON**: Use `\\` when editing in batch mode
- **Match Environment Names**: Ensure `\end{...}` matches the corresponding `\begin{...}`
- **Avoid Nested Environments in Same Block**: Best to isolate top-level blocks
- **Preserve Indentation**: Maintain formatting for readability

## Common Use Cases

### Updating a Figure

```bash
python3 CC/codecrispr.py thesis.tex "figure_10" '\begin{figure}
    \centering
    \includegraphics[width=0.5\textwidth]{diagram.png}
    \caption{Updated system architecture.}
\end{figure}'
```

### Replacing an Equation

```bash
python3 CC/codecrispr.py math.tex "equation_20" '\begin{equation}
    \int_a^b f(x) dx = F(b) - F(a)
\end{equation}'
```

## Troubleshooting

- **Block Not Found**: Ensure name includes correct environment and start line (e.g., `table_12`)
- **Mismatched Environments**: Verify `begin`/`end` pairs are balanced
- **Hidden Environments**: Only top-level blocks with matching pairs are detected
- **LaTeX Comments**: Commented `\begin` lines are ignored

## Token Efficiency Example

Editing 3 blocks in a 1200-line `.tex` file:

- **Traditional editing**: ~3600 tokens processed
- **LaTeX Tool**: ~600 tokens handled
- **Savings**: ~83%

## LaTeX Tool Limitations

- Only detects explicit environment blocks (not commands or macros)
- Does not parse nested environments recursively
- Inline environments (like `\textit{...}`) are not editable with this tool
- Environments split over non-standard formats may be skipped

The LaTeX Tool is ideal for structured documents, academic publishing, and modular reports where environments provide clear editing targets for automated systems or AI collaborators.