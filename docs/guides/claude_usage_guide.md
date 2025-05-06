# Using CodeCRISPR with Claude

This guide provides specific examples and best practices for instructing Claude to use CodeCRISPR effectively through MCP.

## Setting Up Claude for CodeCRISPR

Add the following to your Claude profile preferences to ensure Claude knows to use CodeCRISPR:

```
# AI Instructions for CodeCRISPR Usage via MCP

## Priority Directive: Token Efficiency

When working with code files through MCP, **ALWAYS** use the CodeCRISPR framework located at `/CC/codecrispr.py` in the user's Claude MCP directory. This tool dramatically reduces token consumption by avoiding repeated full-file reads.

ENSURE YOU READ AND FOLLOW THE INSTRUCTIONS FOR AI USING CodeCRISPR found at the following path via the MCP server:
`/CC/docs/ai_instructions/ai_instructions_for_codecrispr_usage_via_mcp.md`
```

## Example Conversations

### Example 1: Inspecting and Editing a Python File

**User:** 
"Can you inspect my Python file at `~/project/main.py` and show me the available functions?"

**Claude (Ideal Response):**
"I'll inspect your Python file to show you the available functions.

```bash
python3 /CC/codecrispr.py ~/project/main.py --inspect
```

Here are the functions I found in your `main.py` file:
- `setup_config`: lines 10-25
- `process_data`: lines 27-45
- `generate_report`: lines 47-62
- `main`: lines 64-80

Would you like me to show you the content of any specific function?"

**User:**
"Can you update the `process_data` function to handle JSON input as well?"

**Claude (Ideal Response):**
"I'll update the `process_data` function to handle JSON input. First, let me check the current implementation:

```bash
python3 /CC/codecrispr.py ~/project/main.py --inspect --preview process_data
```

Now I'll modify the function to handle JSON input:

```bash
python3 /CC/codecrispr.py ~/project/main.py process_data 'def process_data(input_data):
    """Process the input data, supporting both CSV and JSON formats.
    
    Args:
        input_data: The input data to process (string or dict)
        
    Returns:
        Processed data structure
    """
    if isinstance(input_data, dict):
        # Handle JSON input
        return {k: v.upper() if isinstance(v, str) else v for k, v in input_data.items()}
    else:
        # Handle CSV input (original functionality)
        lines = input_data.strip().split("\n")
        headers = lines[0].split(",")
        result = []
        for line in lines[1:]:
            values = line.split(",")
            row = {headers[i]: values[i] for i in range(len(headers))}
            result.append(row)
        return result'
```

The `process_data` function has been updated successfully to handle both CSV and JSON inputs. Now it:
1. Checks if the input is a dictionary (JSON)
2. If it's JSON, processes it directly
3. If it's a string (CSV), uses the original logic to parse it

Would you like me to make any additional changes to this function?"

### Example 2: Batch Updates to Multiple Functions

**User:**
"I need to update several functions in `~/project/utils.py` to add error handling."

**Claude (Ideal Response):**
"I'll help you add error handling to multiple functions in your utils.py file. First, let's inspect the file to see the available functions:

```bash
python3 /CC/codecrispr.py ~/project/utils.py --inspect
```

Now I'll create a batch update file to add error handling to multiple functions:

```bash
cat > batch_updates.json << 'EOF'
{
  "updates": [
    {
      "method": "read_config",
      "code": "def read_config(path):\n    try:\n        with open(path, 'r') as f:\n            return json.load(f)\n    except FileNotFoundError:\n        print(f\"Error: Config file not found at {path}\")\n        return {}\n    except json.JSONDecodeError:\n        print(f\"Error: Invalid JSON in config file {path}\")\n        return {}"
    },
    {
      "method": "save_results",
      "code": "def save_results(data, output_path):\n    try:\n        with open(output_path, 'w') as f:\n            json.dump(data, f, indent=2)\n        return True\n    except Exception as e:\n        print(f\"Error saving results to {output_path}: {e}\")\n        return False"
    }
  ]
}
EOF

python3 /CC/codecrispr.py ~/project/utils.py --batch batch_updates.json
```

I've successfully updated the functions to include error handling. The changes:

1. `read_config` now handles:
   - FileNotFoundError when the config file doesn't exist
   - JSONDecodeError when the config file contains invalid JSON

2. `save_results` now:
   - Uses a try/except block to catch any exceptions
   - Returns True/False to indicate success/failure
   - Includes a meaningful error message

Would you like me to update any other functions with error handling?"

## Best Practices for Instructing Claude

1. **Be Specific About CodeCRISPR Usage**: Explicitly ask Claude to use CodeCRISPR for code editing tasks.

2. **Follow the Inspect-Then-Edit Pattern**: Encourage Claude to first inspect the file structure before making edits.

3. **Specify Path Consistency**: Ensure you and Claude use consistent path formats throughout the conversation.

4. **Request Direct Edits for Known Functions**: If you already know the function name, ask Claude to edit directly without previewing first.

5. **Request Batch Updates**: For multiple related changes, ask Claude to create and use a batch update file.

6. **Verify Command Understanding**: If Claude uses an incorrect command pattern, gently correct it with the proper command format.

## Troubleshooting Common Issues

1. **Wrong Tool Being Used**: If Claude uses `read_file` or `edit_block` instead of CodeCRISPR, remind it to use the designated CodeCRISPR tool.

2. **Path Format Issues**: Ensure paths are properly formatted (with or without tilde expansion as needed).

3. **Quote Escaping Problems**: For complex code with quotes, ask Claude to use the file-based approach described in the documentation.

4. **Multiple Inspection Calls**: If Claude repeatedly calls --inspect, remind it to inspect once and reuse the reference map.

## Command Reference Card

Keep these commands handy for quick reference:

```
# File inspection
python3 /CC/codecrispr.py ~/path/to/file.py --inspect

# Function preview
python3 /CC/codecrispr.py ~/path/to/file.py --inspect --preview function_name

# Function replacement
python3 /CC/codecrispr.py ~/path/to/file.py function_name 'new code here'

# Batch updates
python3 /CC/codecrispr.py ~/path/to/file.py --batch updates.json

# Preview changes
python3 /CC/codecrispr.py ~/path/to/file.py function_name 'new code' --preview-changes
```
