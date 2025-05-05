# XML Tool Guide

## Introduction

The XML Tool in CodeCRISPR supports targeted editing of XML files. It allows you to navigate XML tag hierarchies and replace entire tag blocks by name or path. It is useful for structured data formats such as SVG, config files, or metadata.

## How the XML Tool Works

1. **Tag Path Mapping**: Each element is assigned a slash-separated path (e.g., `root/config/item`)
2. **Element Replacement**: Allows swapping out an entire tag block using its path
3. **Preservation of Structure**: Ensures well-formed XML output via `ElementTree`

## Basic Usage

### Inspect an XML File

```bash
python3 CC/codecrispr.py data.xml --inspect
```

Example Output:
```
Inspecting 'data.xml' [xml_tool]:
  root
  root/config
  root/config/item
```

### Replace a Block

```bash
python3 CC/codecrispr.py data.xml "root/config/item" '<item id="3">new value</item>'
```

### Batch Update

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "root/config/item",
      "code": "<item id=\"1\">Updated</item>"
    }
  ]
}
EOF

python3 CC/codecrispr.py data.xml --batch updates.json
```

## Notes

- All tags are replaced using full `tag/subtag/subsubtag` paths
- The entire tag block must be valid XML (no fragments)
- Case-sensitive tag names

## Limitations

- Comments, namespaces, and mixed content are not preserved precisely
- Only works on well-formed XML with unique tag paths
- All replacement content must be valid XML strings

This tool is ideal for editing structured data, such as Android manifests, SVG components, and configuration files used in academic or web environments.