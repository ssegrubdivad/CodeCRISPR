import re

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_methods()

    def _read_file(self):
        with open(self.filepath, 'r') as f:
            return f.read().splitlines()

    def _parse_methods(self):
        # Enhanced patterns for PHP functions and methods
        patterns = [
            # Regular and static methods with various modifiers
            re.compile(r'^\s*(?:(?:public|protected|private)\s+)?(?:static\s+)?(?:final\s+)?(?:abstract\s+)?function\s+(\w+)\s*\(.*?\)(?:\s*:\s*\??\w+)?(?:\s*\{|;)'),
            # Magic methods (__construct, __destruct, etc.)
            re.compile(r'^\s*(?:(?:public|protected|private)\s+)?function\s+(__\w+)\s*\(.*?\)(?:\s*:\s*\??\w+)?(?:\s*\{|;)'),
            # Anonymous functions assigned to variables
            re.compile(r'^\s*\$(\w+)\s*=\s*function\s*\(.*?\)(?:\s*use\s*\(.*?\))?\s*\{'),
            # Arrow functions (PHP 7.4+)
            re.compile(r'^\s*\$(\w+)\s*=\s*fn\s*\(.*?\)\s*=>\s*[^;]+;'),
        ]
        
        reference_map = {}
        i = 0
        
        while i < len(self.lines):
            line = self.lines[i]
            
            # Match functions and methods
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    name = match.group(1)
                    
                    # Check if it's an abstract method (ends with ;)
                    if line.rstrip().endswith(';'):
                        reference_map[name] = {"start": i, "end": i}
                        i += 1
                        break
                    
                    # For arrow functions (single line)
                    if 'fn' in line and '=>' in line:
                        reference_map[name] = {"start": i, "end": i}
                        i += 1
                        break
                    
                    # Regular functions/methods with body
                    start = i
                    brace_count = 0
                    j = i
                    
                    # Count braces to find the end
                    while j < len(self.lines):
                        # Skip string literals
                        clean_line = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', self.lines[j])
                        # Skip comments
                        clean_line = re.sub(r'//.*$|#.*$|/\*.*?\*/', '', clean_line)
                        
                        brace_count += clean_line.count('{')
                        brace_count -= clean_line.count('}')
                        if brace_count == 0 and j > i:
                            break
                        j += 1
                    
                    end = j
                    reference_map[name] = {"start": start, "end": end}
                    i = end + 1
                    break
            else:
                i += 1
        
        return reference_map

    def replace_method(self, method_name, new_code):
        if method_name not in self.reference_map:
            raise ValueError(f"Function '{method_name}' not found.")
        start = self.reference_map[method_name]["start"]
        end = self.reference_map[method_name]["end"]
        new_lines = new_code.strip('\n').splitlines()
        self.lines[start:end+1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for name, pos in self.reference_map.items():
            if pos["start"] > end:
                pos["start"] += shift
                pos["end"] += shift
        self.reference_map[method_name]["end"] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, 'w') as f:
            f.write('\n'.join(self.lines) + '\n')