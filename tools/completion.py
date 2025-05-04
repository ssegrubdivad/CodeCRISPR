#!/usr/bin/env python3
"""
Shell completion scripts for CodeCRISPR
"""
import os
import sys

BASH_COMPLETION = """
_codecrispr_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--inspect --preview --with-lines --as-comment --preview-only --export --json --pretty --batch --preview-changes --apply --config --help"

    case "${prev}" in
        --preview|--export)
            # Complete with available methods from the file
            if [[ -f "${COMP_WORDS[1]}" ]]; then
                local methods=$(python3 "$(dirname "$1")/codecrispr.py" "${COMP_WORDS[1]}" --inspect --json | python3 -c "import sys, json; data = json.load(sys.stdin); print(' '.join(data['blocks'].keys()))" 2>/dev/null)
                COMPREPLY=( $(compgen -W "${methods}" -- ${cur}) )
            fi
            return 0
            ;;
        --config)
            # Complete with configuration keys
            local config_keys="general.backup_enabled general.backup_extension general.default_language output.use_colors output.json_pretty output.show_line_numbers editor.tab_size editor.use_spaces editor.trim_trailing_whitespace"
            COMPREPLY=( $(compgen -W "${config_keys}" -- ${cur}) )
            return 0
            ;;
        --batch)
            # Complete with JSON files
            COMPREPLY=( $(compgen -f -X '!*.json' -- ${cur}) )
            return 0
            ;;
    esac

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    # Complete with files
    COMPREPLY=( $(compgen -f -- ${cur}) )
}

complete -F _codecrispr_completion codecrispr.py
"""

ZSH_COMPLETION = """
#compdef codecrispr.py

_codecrispr() {
    local -a opts
    opts=(
        '--inspect[Inspect available blocks]'
        '--preview[Preview a named block]:method name:->methods'
        '--with-lines[Include line numbers in preview]'
        '--as-comment[Add comment delimiters to each line]'
        '--preview-only[Only show the preview, no metadata]'
        '--export[Export preview to file]:output file:_files'
        '--json[Output in JSON format]'
        '--pretty[Pretty print JSON output]'
        '--batch[Batch update from JSON file]:json file:_files -g "*.json"'
        '--preview-changes[Preview changes before applying]'
        '--apply[Apply changes after preview]'
        '--config[Show or set configuration values]:config key:->config'
        '--help[Show help message]'
    )

    _arguments -s -S \
        '1:file:_files' \
        '2:method name:->methods' \
        '3:code:' \
        $opts

    case $state in
        methods)
            if [[ -f $words[2] ]]; then
                local methods
                methods=(${(f)"$(python3 ${words[1]:h}/codecrispr.py $words[2] --inspect --json | python3 -c "import sys, json; data = json.load(sys.stdin); print('\\n'.join(data['blocks'].keys()))" 2>/dev/null)"})
                _describe 'method' methods
            fi
            ;;
        config)
            local config_keys
            config_keys=(
                'general.backup_enabled'
                'general.backup_extension'
                'general.default_language'
                'output.use_colors'
                'output.json_pretty'
                'output.show_line_numbers'
                'editor.tab_size'
                'editor.use_spaces'
                'editor.trim_trailing_whitespace'
            )
            _describe 'config key' config_keys
            ;;
    esac
}

_codecrispr "$@"
"""

def install_completions():
    """Install shell completions"""
    shell = os.environ.get('SHELL', '').split('/')[-1]
    
    if shell == 'bash':
        completion_dir = os.path.expanduser('~/.bash_completion.d')
        os.makedirs(completion_dir, exist_ok=True)
        with open(os.path.join(completion_dir, 'codecrispr'), 'w') as f:
            f.write(BASH_COMPLETION)
        print("Bash completion installed. Add this to your .bashrc:")
        print("source ~/.bash_completion.d/codecrispr")
    
    elif shell == 'zsh':
        completion_dir = os.path.expanduser('~/.zsh/completions')
        os.makedirs(completion_dir, exist_ok=True)
        with open(os.path.join(completion_dir, '_codecrispr'), 'w') as f:
            f.write(ZSH_COMPLETION)
        print("Zsh completion installed. Add this to your .zshrc:")
        print("fpath=(~/.zsh/completions $fpath)")
        print("autoload -Uz compinit && compinit")
    
    else:
        print(f"Unsupported shell: {shell}")
        print("Currently supported: bash, zsh")

if __name__ == '__main__':
    install_completions()
