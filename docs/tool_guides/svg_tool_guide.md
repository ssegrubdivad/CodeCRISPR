# SVG Tool Guide

## Introduction

The SVG Tool in CodeCRISPR provides structural editing support for `.svg` graphics files. SVG is XML-based and supports element-wise updates to graphics like circles, rectangles, paths, and text. This tool identifies graphical objects by tag and `id` and allows complete replacement of those elements while preserving document integrity.

## How the SVG Tool Works

1. **Element Mapping**: Each element in the document is identified by tag and optional `id` (e.g., `svg/g/circle[id=marker]`)
2. **XML Parsing**: Uses Python’s `ElementTree` to parse, modify, and write SVG content
3. **Targeted Replacement**: Allows replacing entire graphical elements by path or ID

## Basic Usage Workflow

### Inspect the SVG

```bash
python3 CC/codecrispr.py drawing.svg --inspect
```

Example Output:
```
Inspecting 'drawing.svg' [svg_tool]:
  svg/g[0]/circle[id=marker]
  svg/g[1]/rect[id=background]
  svg/text
```

### Replace an Element

```bash
python3 CC/codecrispr.py drawing.svg "svg/g[0]/circle[id=marker]" '<circle id="marker" cx="25" cy="25" r="20" fill="blue" />'
```

### Batch Replacement

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "svg/g[0]/circle[id=marker]",
      "code": "<circle id=\"marker\" cx=\"10\" cy=\"10\" r=\"5\" fill=\"red\" />"
    }
  ]
}
EOF

python3 CC/codecrispr.py drawing.svg --batch updates.json
```

## Notes

- Matching paths use tag nesting and optional `id` attributes
- Replacement elements must be valid XML/SVG tags
- Works well with vector diagrams, UI wireframes, and icon sets

## Limitations

- Does not preserve indentation or formatting in saved SVG
- Requires unique `id` attributes for reliable mapping
- Does not support inline stylesheets or scripts

This tool is ideal for updating elements in visual diagrams and vector-based user interface components without modifying unrelated portions of the graphic.