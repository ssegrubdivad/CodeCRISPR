# Customization and the INI

CodeCRISPR uses Python's built-in `configparser` module to manage user preferences through an INI file. This system allows users to customize various aspects of CodeCRISPR's behavior without modifying the source code. The configuration file is automatically created at `~/.codecrispr/config.ini` when you first run CodeCRISPR or access the configuration.

You can check the current configuration by running the config command:

```
execute_command [[request]]
{
  `command`: `cd /Users/general/ClaudeServerDirectory && python3 CC/codecrispr.py --config`
}

[[response]]
Command started with PID 87866
Initial output:
[general]
  backup_enabled = true
  backup_extension = .bak
  default_language = python_tool
  auto_format = false
[output]
  use_colors = true
  json_pretty = true
  show_line_numbers = false
[editor]
  tab_size = 4
  use_spaces = true
  trim_trailing_whitespace = true
```

## Current INI File Structure

The configuration file is organized into three main sections:

### [general] Section
This section controls the core behavior of CodeCRISPR:

- **backup_enabled** (default: true): When enabled, CodeCRISPR creates a backup file before making any modifications. This provides a safety net in case something goes wrong during editing.

- **backup_extension** (default: .bak): Specifies the file extension for backup files. If your file is `main.py`, the backup will be `main.py.bak`.

- **default_language** (default: python_tool): When CodeCRISPR can't determine the file type from its extension or content, it falls back to this parser. You can change this to any supported language tool.

- **auto_format** (default: false): This setting is defined but not currently implemented in the code. It's a placeholder for future functionality that could automatically format code after modifications.

### [output] Section
This section controls how CodeCRISPR presents information:

- **use_colors** (default: true): While defined in the config, color output isn't currently implemented in the code. This is another placeholder for future enhancement.

- **json_pretty** (default: true): When using the `--json` flag, this determines whether the JSON output is formatted with indentation (pretty) or compressed to a single line.

- **show_line_numbers** (default: false): This could be used to automatically include line numbers in previews, though the current implementation requires the `--with-lines` flag explicitly.

### [editor] Section
This section defines code editing preferences:

- **tab_size** (default: 4): Intended for future use when CodeCRISPR might need to handle indentation conversions.

- **use_spaces** (default: true): Another future-oriented setting that could control whether CodeCRISPR uses spaces or tabs for indentation.

- **trim_trailing_whitespace** (default: true): Could be used to automatically clean up trailing whitespace when saving files.

## How to Use the Configuration System

You can interact with the configuration in several ways:

To view all settings:
```bash
python3 CC/codecrispr.py --config
```

To view a specific setting:
```bash
python3 CC/codecrispr.py --config general.backup_enabled
```

To change a setting:
```bash
python3 CC/codecrispr.py --config general.backup_enabled=false
```

## How Configuration Affects Operations

Currently, the configuration primarily affects:

1. **Backup Creation**: The `backup_enabled` and `backup_extension` settings control the automatic backup feature that protects your files during modifications.

2. **JSON Formatting**: The `json_pretty` setting determines how JSON output is formatted when you use the `--json` flag.

3. **Language Detection**: The `default_language` setting provides a fallback when file type detection fails.

## Default Configuration

When CodeCRISPR first runs, it creates a configuration file with these defaults at `~/.codecrispr/config.ini`. If this file doesn't exist or is deleted, CodeCRISPR will recreate it with the default values. This ensures that the tool always has a consistent baseline configuration.

The configuration system is designed to be extensible, allowing for future enhancements without breaking existing functionality. Many of the settings are placeholders for planned features, demonstrating the framework's forward-thinking design that anticipates future development needs.
