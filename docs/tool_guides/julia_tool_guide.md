# Julia Tool Guide

## Introduction

The Julia Tool in CodeCRISPR enables efficient editing of Julia `.jl` scripts by identifying and replacing individual function definitions. Julia’s `function ... end` structure makes it a natural fit for CodeCRISPR's approach.

## How the Julia Tool Works

1. **Function Detection**: Identifies blocks that begin with `function name`
2. **Block Closure**: Uses `end` to locate the function’s close
3. **Reference Mapping**: Assigns keys like `foo_12` based on function name and starting line
4. **Precise Editing**: Enables safe and isolated replacement of individual functions

## Basic Workflow

### Inspect the File

```bash
python3 CC/codecrispr.py model.jl --inspect
```

Example output:
```
Inspecting 'model.jl' [julia_tool]:
  simulate_5: lines 5–15
  update_17: lines 17–25
```

### Preview a Function

```bash
python3 CC/codecrispr.py model.jl --inspect --preview "simulate"
```

### Replace a Function

```bash
python3 CC/codecrispr.py model.jl "simulate" 'function simulate(x)
    return x + 1
end'
```

## Batch Updates

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "simulate",
      "code": "function simulate(x)\n    return x + 10\nend"
    },
    {
      "method": "update",
      "code": "function update(y)\n    return y * 2\nend"
    }
  ]
}
EOF

python3 CC/codecrispr.py model.jl --batch updates.json
```

## Limitations

- Only detects functions starting with the `function` keyword on a new line
- Inline function definitions (`f(x) = x^2`) are not currently supported
- Blocks without a clear `end` may be ignored

This tool is ideal for research scripts, numerical models, and data science routines written in Julia.