# CodeCRISPR Framework: Advanced Technical Guide

## Executive Summary

The CodeCRISPR framework provides language-agnostic, AST-like code manipulation capabilities optimized for LLM-assisted development workflows. This guide covers MCP integration with Claude Desktop on macOS, framework architecture, and extension mechanisms for additional language support.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [MCP Integration & Setup](#mcp-integration--setup)
3. [Core Components](#core-components)
4. [Language Tool Implementation](#language-tool-implementation)
5. [Advanced Usage Patterns](#advanced-usage-patterns)
6. [Performance Considerations](#performance-considerations)
7. [Extension Development](#extension-development)
8. [Troubleshooting & Debugging](#troubleshooting--debugging)

## Architecture Overview

### Design Principles

1. **Single-parse efficiency**: Parse target files once, maintain reference maps in memory
2. **Language modularity**: Pluggable language-specific parsers with consistent interfaces
3. **Minimal data transfer**: Transmit only method names and replacement content
4. **Error resilience**: Comprehensive error handling with actionable diagnostics

### Component Architecture

```
codecrispr.py (CLI/Core)
    ├── Language Detection
    ├── Dynamic Module Loading
    └── Command Dispatch
        
tools/
    ├── python_tool.py
    ├── javascript_tool.py
    └── [language]_tool.py
        └── CodeCRISPR class
            ├── __init__(filepath)
            ├── _parse_methods() -> reference_map
            ├── replace_method(name, code)
            └── save()
```

## MCP Integration & Setup

### Claude Desktop Configuration

1. **MCP Server Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/$USER/path/to/your/mcp/directory"],
      "type": "stdio"
    }
  }
}
```

2. **Directory Structure**:
```
/Users/$USER/path/to/your/mcp/directory/
├── CC/
│   ├── codecrispr.py
│   ├── tools/
│   │   └── *_tool.py
│   └── docs/
└── [project_files]
```

3. **Environment Requirements**:
- Python 3.8+
- No external dependencies (stdlib only)
- File system permissions for target directories

### MCP Command Patterns

```python
# Standard MCP interaction pattern
execute_command('python3 CC/codecrispr.py --inspect target.py')
execute_command('python3 CC/codecrispr.py target.py method_name `replacement_code`')
```

## Core Components

### codecrispr.py

**Key Functions**:

```python
def detect_language(file_path):
    """Map file extensions to language tool modules"""
    ext = os.path.splitext(file_path)[1].lower()
    return LANGUAGE_TOOL_MAP.get(ext)

def load_editor(file_path):
    """Dynamically import and instantiate language-specific editor"""
    lang = detect_language(file_path)
    module = importlib.import_module(f'tools.{lang}')
    return module.CodeCRISPR(file_path)
```

**CLI Argument Structure**:
- Positional: `file` (required)
- Positional: `method` (optional)
- Positional: `code` (optional, backtick-wrapped)
- Flags: `--inspect`, `--preview`, `--with-lines`, `--as-comment`, `--export`

### Language Tool Interface

Required methods for `CodeCRISPR` class:

```python
class CodeCRISPR:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_methods()
    
    def _parse_methods(self) -> Dict[str, Dict[str, int]]:
        """Return {method_name: {'start': line_num, 'end': line_num}}"""
        
    def replace_method(self, method_name: str, new_code: str) -> None:
        """Replace method and update reference_map offsets"""
        
    def save(self, output_path: Optional[str] = None) -> None:
        """Write modified content to disk"""
```

## Language Tool Implementation

### Python Parser Example

```python
def _parse_methods(self):
    pattern = re.compile(r'^\s*def\s+(\w+)\s*\(.*?\):')
    reference_map = {}
    i = 0
    while i < len(self.lines):
        match = pattern.match(self.lines[i])
        if match:
            name = match.group(1)
            start = i
            indent = len(self.lines[i]) - len(self.lines[i].lstrip())
            i += 1
            while i < len(self.lines):
                line = self.lines[i]
                if line.strip() == "":
                    i += 1
                    continue
                line_indent = len(line) - len(line.lstrip())
                if line_indent <= indent:
                    break
                i += 1
            end = i - 1
            reference_map[name] = {"start": start, "end": end}
        else:
            i += 1
    return reference_map
```

### Pattern-Based Parsing Strategy

1. **Regex patterns**: Language-specific function/block signatures
2. **Indentation tracking**: Python, YAML
3. **Bracket matching**: C-like languages
4. **Delimiter pairs**: LaTeX, HTML

## Advanced Usage Patterns

### Multi-file Refactoring Workflow

```python
# 1. Build reference maps for all files
file_maps = {}
for file in project_files:
    result = execute_command(f'python3 CC/codecrispr.py --inspect {file}')
    file_maps[file] = parse_inspection_output(result)

# 2. Coordinate changes across files
for file, methods in refactoring_plan.items():
    for method, new_code in methods.items():
        execute_command(f'python3 CC/codecrispr.py {file} {method} `{new_code}`')
```

### Preservation of Formatting

```python
# Extract with formatting preservation
execute_command('python3 CC/codecrispr.py --inspect file.py --preview method --as-comment --export temp.txt')

# Modify externally
modified_content = process_exported_content('temp.txt')

# Re-inject
execute_command(f'python3 CC/codecrispr.py file.py method `{modified_content}`')
```

## Performance Considerations

### Memory Efficiency

- Reference maps are O(n) where n = number of methods
- Line-based storage avoids full AST overhead
- Incremental offset updates after edits

### I/O Optimization

- Single file read on initialization
- Buffered writes on save
- No temporary file creation

### Scaling Characteristics

| File Size | Parse Time | Memory Usage | Edit Time |
|-----------|------------|--------------|-----------|
| 1K lines  | ~10ms      | ~100KB       | ~5ms      |
| 10K lines | ~100ms     | ~1MB         | ~10ms     |
| 100K lines| ~1s        | ~10MB        | ~20ms     |

## Extension Development

### Creating a New Language Tool

1. **File Structure**:
```python
# tools/rust_tool.py
import re

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_methods()
```

2. **Parser Implementation**:
```python
def _parse_methods(self):
    # Rust function pattern
    pattern = re.compile(r'^\s*(pub\s+)?fn\s+(\w+)\s*\(')
    reference_map = {}
    # Implementation details...
    return reference_map
```

3. **Registration**:
```python
# In codecrispr.py
LANGUAGE_TOOL_MAP = {
    '.rs': 'rust_tool',  # Add this line
    # ... other mappings
}
```

### Advanced Parser Techniques

#### Context-Aware Parsing

```python
def _parse_with_context(self):
    """Parse with awareness of nested structures"""
    stack = []
    contexts = {'class': None, 'namespace': None}
    
    for i, line in enumerate(self.lines):
        # Track context changes
        if self._is_context_start(line):
            stack.append(self._extract_context(line))
        elif self._is_context_end(line):
            if stack:
                stack.pop()
        
        # Parse with full context
        if self._is_method_def(line):
            full_name = self._build_qualified_name(stack, line)
            # Store with context...
```

#### Multi-Pattern Support

```python
PATTERNS = {
    'function': re.compile(r'function\s+(\w+)'),
    'arrow': re.compile(r'const\s+(\w+)\s*=\s*\(.*?\)\s*=>'),
    'method': re.compile(r'(\w+)\s*\(.*?\)\s*{'),
}

def _parse_methods(self):
    reference_map = {}
    for i, line in enumerate(self.lines):
        for pattern_type, pattern in PATTERNS.items():
            if match := pattern.match(line):
                # Handle based on pattern_type...
```

## Troubleshooting & Debugging

### Common Issues

1. **Reference Map Staleness**
   - Symptom: "Method not found" after external edits
   - Solution: Re-run `--inspect` to rebuild map

2. **Boundary Detection Failures**
   - Symptom: Incomplete method replacement
   - Debug: Use `--preview` with `--with-lines` to verify boundaries

3. **Character Encoding Issues**
   - Symptom: Unicode errors on save
   - Solution: Explicit encoding in file operations

### Debug Mode Implementation

```python
# Add to codecrispr.py
if os.environ.get('CODECRISPR_DEBUG'):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    def debug_wrap(func):
        def wrapper(*args, **kwargs):
            logging.debug(f"Calling {func.__name__} with {args}, {kwargs}")
            result = func(*args, **kwargs)
            logging.debug(f"Result: {result}")
            return result
        return wrapper
    
    # Apply to key functions
    load_editor = debug_wrap(load_editor)
```

### Error Recovery Strategies

```python
def safe_replace_method(self, method_name, new_code):
    """Replacement with rollback capability"""
    backup_lines = self.lines.copy()
    backup_map = self.reference_map.copy()
    
    try:
        self.replace_method(method_name, new_code)
    except Exception as e:
        self.lines = backup_lines
        self.reference_map = backup_map
        raise RuntimeError(f"Replacement failed, state rolled back: {e}")
```

## Best Practices for MCP Integration

1. **Path Management**:
   ```python
   # Always use absolute paths with MCP
   abs_path = os.path.abspath(file_path)
   execute_command(f'python3 /Users/$USER/ClaudeServerDirectory/CC/codecrispr.py {abs_path} ...')
   ```

2. **Error Handling**:
   ```python
   result = execute_command(cmd)
   if "[ERROR]" in result:
       # Parse error message and handle appropriately
       error_handler(result)
   ```

3. **State Management**:
   ```python
   class FileState:
       def __init__(self, file_path):
           self.path = file_path
           self.reference_map = None
           self.last_inspected = None
       
       def should_reinspect(self):
           return (not self.reference_map or 
                   time.time() - self.last_inspected > 300)  # 5 min timeout
   ```

## Performance Tuning

### Large File Optimization

```python
def _parse_methods_chunked(self, chunk_size=1000):
    """Process large files in chunks to avoid memory spikes"""
    reference_map = {}
    for chunk_start in range(0, len(self.lines), chunk_size):
        chunk_end = min(chunk_start + chunk_size, len(self.lines))
        chunk_map = self._parse_chunk(chunk_start, chunk_end)
        reference_map.update(chunk_map)
    return reference_map
```

### Caching Strategy

```python
class CachedCodeCRISPR(CodeCRISPR):
    _cache = {}
    
    def __init__(self, filepath):
        cache_key = (filepath, os.path.getmtime(filepath))
        if cache_key in self._cache:
            self.__dict__.update(self._cache[cache_key])
        else:
            super().__init__(filepath)
            self._cache[cache_key] = self.__dict__.copy()
```

## Security Considerations

1. **Path Traversal Protection**:
   ```python
   def validate_path(self, path):
       abs_path = os.path.abspath(path)
       allowed_dir = os.path.abspath(self.allowed_directory)
       if not abs_path.startswith(allowed_dir):
           raise SecurityError("Path traversal attempt detected")
   ```

2. **Code Injection Prevention**:
   ```python
   def sanitize_code(self, code):
       # Remove potential shell escapes
       if any(char in code for char in ['`', '$', ';']):
           raise ValueError("Potentially unsafe characters in code")
       return code
   ```

## Token Optimization Strategies

### Architectural Decisions for Token Efficiency

CodeCRISPR's architecture prioritizes token conservation through several key design decisions:

1. **Persistent Reference Maps**
   - Reference maps are maintained in memory after initial parse
   - Subsequent operations use cached structural data
   - No repeated file parsing for multiple operations

2. **Minimal Data Transfer**
   - Only method names and replacement content are transmitted
   - File structure queries use pre-computed indices
   - Verification happens server-side, not through chat

### Token Complexity Analysis

| Operation | Traditional Approach | CodeCRISPR | Token Reduction |
|-----------|---------------------|---------------|-----------------|
| Initial Inspection | O(n) | O(n) | 0% |
| Subsequent Edit | O(n) | O(1) | ~99% |
| Multiple Edits (m) | O(m*n) | O(n) + O(m) | ~95% |
| Preview Operation | O(n) | O(1) | ~99% |

Where n = file size in lines, m = number of operations

### Implementation Pattern for Token Efficiency

```python
class TokenEfficientWorkflow:
    def __init__(self, file_path):
        """Single inspection, multiple operations pattern"""
        self.file_path = file_path
        self.reference_map = self._inspect_once()
        self.operations_count = 0
    
    def _inspect_once(self):
        """Perform one-time inspection"""
        result = execute_command(
            f'python CC/codecripr.py --inspect {self.file_path}'
        )
        return parse_reference_map(result)
    
    def edit_method(self, method_name, new_code):
        """Direct edit without re-inspection"""
        self.operations_count += 1
        return execute_command(
            f'python CC/codecripr.py {self.file_path} {method_name} `{new_code}`'
        )
    
    def get_token_savings(self, file_lines):
        """Calculate token savings vs traditional approach"""
        traditional_tokens = file_lines * (self.operations_count + 1)
        me_tokens = file_lines + (self.operations_count * 10)  # Approx
        return (traditional_tokens - me_tokens) / traditional_tokens
```

### Best Practices for Production LLM Integrations

1. **Session Persistence**
   - Maintain reference maps across conversation turns
   - Implement conversation state management
   - Clear maps only on file structure changes

2. **Intelligent Preview Strategy**
   ```python
   def should_preview(self, method_name, last_viewed_timestamp):
       """Determine if preview is necessary"""
       # Skip if method was recently viewed
       if time.time() - last_viewed_timestamp < 300:  # 5 minutes
           return False
       # Skip if method hasn't been modified externally
       if not self.is_externally_modified(method_name):
           return False
       return True
   ```

3. **Batch Operation Optimization**
   ```python
   def batch_edit_methods(self, edits):
       """Perform multiple edits efficiently"""
       # Single inspection
       self._ensure_reference_map()
       
       # Multiple edits without re-parsing
       results = []
       for method_name, new_code in edits.items():
           results.append(self.edit_method(method_name, new_code))
       
       return results
   ```

### Token Usage Monitoring

```python
class TokenUsageMonitor:
    def __init__(self):
        self.token_counts = defaultdict(int)
    
    def log_operation(self, operation_type, file_size):
        """Track token usage by operation type"""
        if operation_type == 'inspect':
            self.token_counts['inspect'] += file_size
        elif operation_type == 'edit':
            self.token_counts['edit'] += 10  # Approximate
        elif operation_type == 'preview':
            self.token_counts['preview'] += 5  # Approximate
    
    def get_efficiency_report(self):
        """Generate token efficiency report"""
        total = sum(self.token_counts.values())
        return {
            'total_tokens': total,
            'breakdown': dict(self.token_counts),
            'efficiency_ratio': self.token_counts['edit'] / total
        }
```

### Anti-Patterns That Waste Tokens

1. **Redundant Inspection Pattern**
   ```python
   # INEFFICIENT - Avoid this!
   for method in methods_to_edit:
       execute_command(f'python CC/codecripr.py --inspect {file}')
       execute_command(f'python CC/codecripr.py --preview {method}')
       execute_command(f'python CC/codecripr.py {file} {method} `{code}`')
   ```

2. **Unnecessary Preview Pattern**
   ```python
   # INEFFICIENT - Avoid this!
   # Preview before edit (when you already know the content)
   execute_command(f'python CC/codecripr.py --preview {method}')
   # Edit
   execute_command(f'python CC/codecripr.py {file} {method} `{code}`')
   # Preview again to verify (trust the tool!)
   execute_command(f'python CC/codecripr.py --preview {method}')
   ```

3. **Correct Efficient Pattern**
   ```python
   # EFFICIENT - Use this!
   # Inspect once
   execute_command(f'python CC/codecripr.py --inspect {file}')
   
   # Multiple direct edits
   for method, code in edits.items():
       execute_command(f'python CC/codecripr.py {file} {method} `{code}`')
   ```

## Understanding Token Economics with CodeCRISPR

### What Are Tokens?
- Tokens are the currency of AI conversations
- Each file read, response generated, and operation performed consumes tokens
- Most AI services have token limits per conversation or time period

### CodeCRISPR's Token-Saving Architecture
1. **One-Time File Parsing**: Build reference map once, reuse many times
2. **Surgical Edits**: Change only what's needed, not entire files
3. **Cached Context**: Maintain file structure knowledge across operations

### Real-World Token Savings

| Scenario | Traditional Tokens | CodeCRISPR Tokens | Savings |
|----------|-------------------|---------------------|---------|
| Edit 1 function in 500-line file | ~1,000 | ~510 | 49% |
| Edit 5 functions in 500-line file | ~5,000 | ~550 | 89% |
| Edit 10 functions in 1,000-line file | ~20,000 | ~1,100 | 94% |

### The "First Action" Principle
- Always inspect first when starting work on a file
- This investment pays off with every subsequent operation
- Think of it as "indexing" the file for efficient access

## Conclusion

The CodeCRISPR framework provides a robust foundation for LLM-assisted code manipulation with minimal overhead. Its modular architecture supports easy extension while maintaining consistent interfaces across languages. When integrated with Claude Desktop via MCP, it enables efficient, targeted code modifications that scale well with file size and complexity.

For production deployments, consider implementing the suggested caching strategies, error recovery mechanisms, and security hardening measures. The framework's simplicity is its strength—maintain this principle when extending functionality.
