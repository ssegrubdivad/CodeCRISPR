# Language-Specific Caveats for CodeCRISPR

This guide documents important limitations and edge cases for each language parser supported by CodeCRISPR. Understanding these caveats will help you use CodeCRISPR more effectively and avoid common issues.

## General Considerations for All Languages

While CodeCRISPR provides efficient code editing for most standard code structures, it's important to understand that any pattern-based parsing system has inherent limitations. The following considerations apply across all supported languages:

1. **Non-Standard Syntax**: Unconventional coding styles or syntax patterns may not be detected correctly.
2. **Dynamic Code Structures**: Code generated at runtime or defined conditionally may not be detected.
3. **Deeply Nested Structures**: Complex nesting may occasionally cause boundary detection issues.
4. **Mixed Language Content**: Files containing multiple languages (e.g., embedded JavaScript in HTML) may have detection challenges.
5. **Preprocessing Directives**: Macro expansions and preprocessor directives can interfere with parsing.

## Troubleshooting Recommendations for All Languages

When encountering parsing issues with any language tool:

1. **Verify File Format**: Ensure the file uses standard formatting and syntax for the language.
2. **Simplify Complex Structures**: Temporarily simplify nested or complex structures before editing.
3. **Use Inspection First**: Always use `--inspect` to verify that the target block is correctly identified.
4. **Preview Before Editing**: Use `--preview` to check the exact content that will be modified.
5. **Consider Alternative Approaches**: For particularly complex cases, consider using `edit_block` or `write_file` instead of function/method replacement.
6. **File-Based Input**: For complex code with special characters, use the file-based input approach described in the documentation.

## Python Caveats

Python parsing in CodeCRISPR relies on indentation patterns and function declaration syntax. While this works reliably for most Python code, there are specific edge cases to be aware of:

### Parsing Limitations

- **Decorators**: While the Python tool correctly identifies functions with decorators, it may struggle with complex nested decorators or decorators with multiline arguments.
- **Nested Functions**: Deeply nested functions might not be correctly identified if they have unusual indentation patterns.
- **Conditional Function Definitions**: Functions defined inside conditional blocks (if/else statements) may not be consistently detected.
- **Generated Functions**: Functions created via metaprogramming or `exec()` will not be detected as they exist only at runtime.
- **Async Complexity**: Very complex async functions with nested coroutines might have boundary detection issues.

### Handling Edge Cases

- For complex decorators, consider temporarily simplifying them before editing.
- For nested functions, edit the parent function instead of trying to target the nested function directly.
- When working with conditional function definitions, edit the entire conditional block using `edit_block` instead.
- Break down complex async functions into smaller, more manageable pieces for more reliable editing.

## JavaScript/TypeScript Caveats

JavaScript and TypeScript parsing in CodeCRISPR uses pattern matching for function declarations, method definitions, and arrow functions. Modern JavaScript features introduce some complexity that can affect parsing:

### Parsing Limitations

- **Complex Arrow Functions**: Arrow functions with implicit returns or complex destructuring patterns might not be reliably detected.
- **Object Method Shorthand**: Methods defined using shorthand syntax in object literals may be parsed inconsistently.
- **Higher-Order Components**: React HOCs and other function wrappers can confuse the parser when heavily nested.
- **Dynamic Property Names**: Methods using computed property names (e.g., `[dynamicName]() {}`) may not be correctly identified.
- **JSX Boundaries**: The tool might struggle with JSX when it contains functions or methods defined inline.

### Handling Edge Cases

- Convert arrow functions to standard function syntax temporarily for complex edits.
- For object methods, consider editing the entire containing object instead of a single method.
- When working with HOCs or heavily wrapped components, use `--preview` to verify correct function boundaries.
- Extract complex JSX into separate components before editing for more reliable parsing.

## HTML/XML Caveats

HTML and XML parsing relies on tag matching and nesting structure. While effective for most well-formed documents, it has specific limitations:

### Parsing Limitations

- **Malformed HTML/XML**: Documents with missing closing tags or improper nesting may not be correctly parsed.
- **CDATA Sections**: Content within CDATA sections might cause unexpected parsing results.
- **HTML5 Self-closing Tags**: Non-standard self-closing tags without the closing slash may confuse the parser.
- **Embedded Scripts/Styles**: Complex JavaScript or CSS embedded within HTML might interfere with element boundary detection.
- **Custom Elements**: Some custom element definitions (especially those with complex attributes) might not be consistently detected.

### Handling Edge Cases

- Validate HTML/XML formatting before editing using a linter or formatter.
- For CDATA sections, consider editing the entire parent element instead of targeting content within CDATA.
- Use standard XML self-closing syntax (with trailing slash) for more consistent parsing.
- Extract complex embedded scripts or styles to external files before editing.
- For documents with many custom elements, use `--inspect` with `--preview` to verify correct element boundaries.

## CSS Caveats

CSS parsing in CodeCRISPR works on a rule-based structure, identifying selectors and their associated declarations:

### Parsing Limitations

- **Complex Selectors**: Extremely long or complex selectors may not be properly identified.
- **Nested Rules**: Some preprocessor-specific nested rule syntax may not be correctly processed.
- **Vendor Prefixes**: Extensive use of vendor prefixes might affect rule boundary detection.
- **CSS-in-JS**: CSS defined within JavaScript template literals may not be detected as CSS rules.
- **At-Rules**: Complex at-rules with nested content may have boundary detection issues.

### Handling Edge Cases

- Simplify complex selectors temporarily before editing.
- Extract nested rules into standalone rules for editing, then revert to nested syntax.
- For CSS-in-JS, edit the entire JavaScript function containing the CSS rather than targeting specific rules.
- Use `--preview` to verify correct rule boundaries before editing.

## Markdown Caveats

Markdown parsing focuses on heading-based sections, which works well for most documentation but has some inherent limitations:

### Parsing Limitations

- **Markdown inside HTML**: The tool will not detect or correctly parse headings that appear inside HTML blocks or custom components.
- **Table Formatting**: When replacing sections containing tables, the table formatting must be precisely maintained to prevent rendering issues.
- **Frontmatter**: YAML frontmatter is treated as part of the first section. When editing the first heading, include the frontmatter to avoid losing it.
- **Non-standard Heading Formats**: Documents using Setext-style headings (underlined with === or ---) instead of ATX-style (#) may not be correctly parsed.
- **Heading IDs**: Custom heading IDs (e.g., `## Heading {#custom-id}`) may interfere with heading detection in some cases.

### Handling Edge Cases

- For documents with HTML blocks containing headings, use `edit_block` instead of heading-based editing.
- When working with frontmatter, always inspect the document structure first to understand section boundaries.
- Convert Setext-style headings to ATX-style before editing for more reliable parsing.
- Remove custom heading IDs temporarily if experiencing detection issues.

## C++ Caveats

C++ parsing focuses on function and method declarations, but the complexity of C++ syntax creates several edge cases:

### Parsing Limitations

- **Templates**: Complex template declarations may not be correctly parsed, especially with nested templates.
- **Macros**: Macro-heavy code can confuse the parser, especially when macros generate function-like structures.
- **Operator Overloading**: Operator overloading functions might not be consistently detected.
- **Friend Declarations**: Friend functions may be detected inconsistently.
- **Multiple Inheritance**: Complex inheritance hierarchies can complicate method detection.

### Handling Edge Cases

- For template-heavy code, consider using `edit_block` instead of function replacement.
- When working with macros, edit the entire surrounding context to ensure consistency.
- For operator overloading, use the exact operator syntax as shown in `--inspect` results.
- With friend declarations, target the containing class rather than the friend function.

## Java Caveats

Java parsing identifies classes, methods, and nested structures, but has some limitations with modern Java features:

### Parsing Limitations

- **Anonymous Classes**: Methods in anonymous inner classes may not be correctly identified.
- **Lambda Expressions**: Methods containing complex lambda expressions might have boundary detection issues.
- **Annotation Complexity**: Methods with multiple complex annotations may not be consistently parsed.
- **Generic Methods**: Methods with complex generic type parameters might not be detected correctly.
- **Method References**: Code heavy with method references can confuse boundary detection.

### Handling Edge Cases

- For anonymous classes, edit the entire outer method containing the anonymous class.
- Extract complex lambda expressions to named methods before editing.
- Simplify annotations temporarily for more reliable editing.
- For complex generic methods, use `--preview` to verify boundaries before editing.

## Other Languages

Each additional language supported by CodeCRISPR has its own specific parsing limitations. Refer to the individual language tool guides in the `docs/tool_guides/` directory for detailed information about:

- Rust
- Go
- PHP
- SQL
- Julia
- Shell scripts
- And more

## Best Practices Across All Languages

To maximize success when using CodeCRISPR with any language:

1. **Start Simple**: Begin with simple, well-defined functions or methods before attempting complex edits.
2. **Verify First**: Always use `--inspect` to verify the reference map before editing.
3. **Preview Changes**: Use `--preview-changes` to see exactly what will be modified.
4. **Batch Wisely**: When using batch operations, group related changes that won't affect each other.
5. **Fallback Options**: Remember that `edit_block` is always available as a fallback when method detection isn't reliable.
6. **File-Based Input**: For complex replacement code with special characters or multi-line content, always use the file-based input approach.

## Conclusion

Understanding the parser limitations for each language helps you work more effectively with CodeCRISPR. When you encounter edge cases, using the recommended workarounds will ensure successful code editing while maintaining token efficiency.

For specific details about each language parser, refer to the dedicated language tool guides in the `docs/tool_guides/` directory.
