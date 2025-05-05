# Java Tool Guide

## Introduction

The Java Tool in CodeCRISPR allows safe and modular editing of Java methods in `.java` files. It detects class methods using common access and return type patterns and enables precise replacement of method definitions.

## How the Java Tool Works

1. **Method Detection**: Uses a regular expression to identify method signatures
2. **Brace Matching**: Locates method boundaries by tracking `{` and `}` count
3. **Reference Mapping**: Associates each method with its name and line range
4. **Token-Efficient Replacement**: Enables direct modification of only the relevant method body

## Basic Usage

### Inspect a Java File

```bash
python3 CC/codecrispr.py MyClass.java --inspect
```

Output:
```
Inspecting 'MyClass.java' [java_tool]:
  toString: lines 12–20
  calculateTotal: lines 22–33
```

### Replace a Method

```bash
python3 CC/codecrispr.py MyClass.java "calculateTotal" 'public int calculateTotal(int a, int b) {
  return a + b;
}'
```

## Batch Replacement

```bash
cat > updates.json << 'EOF'
{
  "updates": [
    {
      "method": "toString",
      "code": "public String toString() { return \"Hello\"; }"
    }
  ]
}
EOF

python3 CC/codecrispr.py MyClass.java --batch updates.json
```

## Notes

- Works with methods that start with `public`, `private`, or `protected`
- Also handles `static`, `final`, and generic return types
- Does not modify constructors or anonymous inner classes

## Limitations

- Cannot detect methods split across multiple annotations or inline interfaces
- Ignores commented-out or malformed code
- Only parses top-level methods (no lambdas, local class methods, or interfaces)

This tool is well-suited for enterprise Java codebases, Android apps, and backend API development workflows.