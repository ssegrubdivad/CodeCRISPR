# Error Handling in CodeCRISPR

This guide provides detailed information about common error scenarios in CodeCRISPR, their causes, and recommended solutions. Understanding these error patterns will help you troubleshoot issues more effectively and ensure successful code edits.

## Error Types and Handling

CodeCRISPR can encounter several types of errors during operation. This section outlines the most common error categories and how to address them.

### 1. File Access Errors

These occur when CodeCRISPR cannot access the specified file:

```
[ERROR] File not found: /path/to/nonexistent.py
[ERROR] Not a file: /path/to/directory
[ERROR] File not readable: /path/to/protected.py
```

**Potential Causes:**
- The file path is incorrect
- The file doesn't exist
- The path points to a directory instead of a file
- The file exists but the current user doesn't have read permissions

**Solutions:**
- Double-check the file path for typos
- Verify the file exists using `ls` or File Explorer
- Ensure you're targeting a file and not a directory
- Check file permissions with `ls -l <filepath>`
- Change permissions if needed with `chmod u+w <filepath>`

### 2. Method Not Found Errors

These occur when trying to replace a method that doesn't exist in the reference map:

```
[ERROR] Method 'function_name' not found.
```

**Potential Causes:**
- Method name is misspelled
- Method exists but wasn't detected by the parser
- Method is defined dynamically or conditionally
- Method is nested inside another function/class
- The parser has limitations with certain syntax patterns

**Solutions:**
- Use `--inspect` to get the exact method names from the reference map
- Verify case sensitivity and exact spelling
- For nested methods, target the parent method/class instead
- Use `edit_block` as a fallback for methods that aren't being detected
- Check the language-specific caveats documentation for known limitations

### 3. Syntax Errors After Editing

**Scenario:** The edited file contains syntax errors after using CodeCRISPR.

**Potential Causes:**
- Incorrect indentation in the replacement code
- Missing parentheses, braces, or other syntax elements
- Inconsistent line endings (CRLF vs LF)
- Invisible/non-printing characters in the replacement code
- Incomplete code blocks in the replacement

**Solutions:**
- Use `--preview-changes` before applying changes to verify syntax
- Ensure consistent indentation matching the file's style
- Check for balanced parentheses, braces, and quotation marks
- Use the file-based input approach to avoid shell interpretation issues
- Run a syntax validator after editing (e.g., `python -m py_compile` for Python files)
- For indentation-sensitive languages like Python, ensure consistent indentation style

### 4. File Permission Errors

```
[ERROR] Failed to write file: Permission denied
```

**Potential Causes:**
- The file is read-only
- The file is owned by another user
- The file is locked by another process
- The file is in a directory with restricted permissions

**Solutions:**
- Check file permissions with `ls -l <filepath>`
- Change permissions with `chmod u+w <filepath>`
- Close any applications that might have the file open
- Copy the file to a location with appropriate permissions, edit there, then move back
- Verify the user running CodeCRISPR has write permissions to the directory

### 5. Backup Creation Failures

```
[ERROR] Failed to write file: [Errno 2] No such file or directory
```

**Potential Causes:**
- The backup directory doesn't exist
- The backup path is invalid
- Insufficient disk space for backup
- Path contains special characters that need escaping

**Solutions:**
- Check if the target directory exists and create it if needed
- Verify the backup path is valid and writable
- Check available disk space using `df -h`
- Disable backups temporarily with `--config general.backup_enabled=false` if needed
- Use simple paths without special characters

### 6. Encoding Issues

**Scenario:** The edited file contains garbled text or incorrect characters.

**Potential Causes:**
- File uses non-UTF-8 encoding
- Special characters being incorrectly interpreted
- Byte Order Mark (BOM) issues
- Mixed line endings

**Solutions:**
- Check file encoding before editing (use `file -I <filepath>`)
- For non-UTF-8 files, convert to UTF-8 before editing
- Remove BOM if present
- Normalize line endings with a dedicated tool
- Use the file-based input approach for complex text
- Consider editing the file in a good text editor with encoding support first

### 7. Reference Map Updates Failure

**Scenario:** After editing a function, subsequent edits to other functions fail or produce unexpected results.

**Potential Causes:**
- Code structure changed significantly, invalidating the reference map
- A previous edit introduced syntax errors
- Line number shifts weren't properly tracked
- The file was modified externally between operations

**Solutions:**
- Re-inspect the file to rebuild the reference map after major changes
- Use `--inspect` to verify the current reference map
- Edit from bottom to top for multiple changes to minimize line number shifts
- Consider using batch operations for multiple related changes
- Make sure the file isn't being edited by multiple processes simultaneously

### 8. Parser Detection Issues

**Scenario:** CodeCRISPR fails to correctly identify functions or sections in the file.

**Potential Causes:**
- Unusual coding style or non-standard syntax
- Mixed language content in a single file
- The file type isn't correctly detected
- The language parser has limitations for certain constructs
- Complex nested structures confuse the parser

**Solutions:**
- Use an explicit language tool via the config if detection fails
- Format the code with a standard formatter before editing
- Use simpler, more standard syntax for problematic code sections
- Split mixed-language files into separate files if possible
- Use `edit_block` for sections that aren't properly detected
- Refer to the language-specific caveats documentation

### 9. Batch Operation Failures

```
[ERROR] Batch update failed: Expecting property name enclosed in double quotes
```

**Potential Causes:**
- Invalid JSON syntax in the batch file
- Missing quotes around property names
- Missing commas between items
- Incorrect nesting of objects and arrays
- The JSON file contains syntax errors

**Solutions:**
- Validate JSON syntax with a dedicated tool or online validator
- Ensure all property names are in double quotes
- Check for missing commas between array items or object properties
- Use a JSON formatter to clean up the batch file
- Use a properly escaped format for the code strings
- Consider using a JSON linter to validate your batch file

### 10. Command Line Argument Issues

**Scenario:** Arguments containing special characters aren't interpreted correctly.

**Potential Causes:**
- Shell interpretation of quotes, variables, or escape sequences
- Backticks being interpreted as command substitution
- Dollar signs being interpreted as variable references
- Newlines or tabs in the replacement code
- Different shells handling escaping differently

**Solutions:**
- Use single quotes for the outermost quoting in bash/zsh
- Escape special characters appropriately
- **Use the file-based input approach for complex replacement code** (strongly recommended)
- Use heredocs for multiline replacement code
- Consider creating a temporary file and using command substitution

## The File-Based Input Solution

For many of the error scenarios above, especially those involving special characters or multi-line code, the file-based input approach is the most reliable solution:

```bash
# Create a temporary file with the exact code
cat > new_code.js << 'EOF'
function render() {
  // Your complex code with special characters
  // No escaping needed!
  const data = items.map(item => `<li>${item.name}</li>`).join('');
  return `<ul>${data}</ul>`;
}
EOF

# Use command substitution to pass the content
python3 CC/codecrispr.py app.js render "$(cat new_code.js)"
```

This approach bypasses shell interpretation issues completely and works reliably across different shells and operating systems.

## Recovery Procedures

If CodeCRISPR has made changes to a file and you need to recover:

### 1. Using Automatic Backups

By default, CodeCRISPR creates backup files with a `.bak` extension:

```bash
# List backup files
ls -la *.bak

# Restore from backup
cp myfile.py.bak myfile.py
```

### 2. Using Version Control

If you're using Git or another version control system:

```bash
# Check what changed
git diff myfile.py

# Revert changes
git checkout -- myfile.py
```

### 3. Manual Recovery

If automatic backups were disabled:

1. If you still have the terminal open, check the output to see what was changed
2. Use a text editor to manually correct the issues
3. Consider enabling backups for future operations: 
   ```bash
   python3 CC/codecrispr.py --config general.backup_enabled=true
   ```

## Preventive Measures

To minimize errors when using CodeCRISPR:

1. **Always Inspect First**: Use `--inspect` to understand the file structure before editing
2. **Preview Changes**: Use `--preview-changes` to see what will be modified
3. **Use Backups**: Keep the backup feature enabled
4. **Test Small Changes**: Start with small, simple edits before attempting complex operations
5. **Version Control**: Work in a version-controlled environment when possible
6. **File-Based Input**: Use the file-based input approach for complex code
7. **Batch Related Changes**: Use batch operations for multiple related changes
8. **Standard Syntax**: Use conventional coding style for better parsing

## Debugging Process

When encountering persistent issues:

1. **Enable JSON Output**: Use the `--json` flag to get more structured information
   ```bash
   python3 CC/codecrispr.py myfile.py --inspect --json
   ```

2. **Check Configuration**: Verify your current configuration settings
   ```bash
   python3 CC/codecrispr.py --config
   ```

3. **Verbose Mode**: For more detailed information, use
   ```bash
   python3 -v CC/codecrispr.py myfile.py --inspect
   ```

4. **Review File Structure**: Use external tools to analyze the file structure
   ```bash
   # For Python files
   python -m ast myfile.py
   
   # For JavaScript
   npx acorn myfile.js
   ```

## Conclusion

Most CodeCRISPR errors can be resolved by:

1. Using the `--inspect` command to verify file structure
2. Checking for syntax issues in your replacement code
3. Using the file-based input approach for complex edits
4. Being aware of language-specific parser limitations
5. Using `edit_block` as a fallback for complex or problematic code sections

By understanding common error patterns and following these guidelines, you can ensure more reliable and efficient code editing with CodeCRISPR.
