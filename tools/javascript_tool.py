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
        # Enhanced patterns to match various JavaScript function declarations
        patterns = [
            # Traditional function declarations (with optional async)
            re.compile(r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{"),
            # Arrow functions assigned to const/let/var
            re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=])\s*=>\s*\{"),
            # Class methods (including async and static)
            re.compile(r"^\s*(?:static\s+)?(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{"),
            # Object property functions
            re.compile(r"^\s*(\w+)\s*:\s*(?:async\s+)?function\s*\([^)]*\)\s*\{"),
            # Object property arrow functions
            re.compile(r"^\s*(\w+)\s*:\s*(?:async\s+)?(?:\([^)]*\)|[^=])\s*=>\s*\{"),
        ]
        
        reference_map = {}
        i = 0
        in_class = False
        class_indent = 0
        
        while i < len(self.lines):
            line = self.lines[i]
            
            # Track class context
            if re.match(r"^\s*class\s+\w+", line):
                in_class = True
                class_indent = len(line) - len(line.lstrip())
            elif in_class and line.strip() == "}" and len(line) - len(line.lstrip()) == class_indent:
                in_class = False
            
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    name = match.group(1)
                    # Avoid constructor as a named method
                    if name == "constructor":
                        name = "constructor"
                    
                    # Check if we already have this name
                    if name not in reference_map:
                        start = i
                        brace_count = 0
                        j = i
                        
                        # Count braces to find the end
                        while j < len(self.lines):
                            brace_count += self.lines[j].count("{")
                            brace_count -= self.lines[j].count("}")
                            if brace_count == 0 and j > i:
                                break
                            j += 1
                        
                        end = j
                        reference_map[name] = {"start": start, "end": end}
                        break
            i += 1
        
        return reference_map
    def replace_method(self, method_name, new_code):
        if method_name not in self.reference_map:
            raise ValueError(f"Function '{method_name}' not found.")
        start = self.reference_map[method_name]['start']
        end = self.reference_map[method_name]['end']
        new_lines = new_code.strip('\n').splitlines()
        self.lines[start:end+1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for name, pos in self.reference_map.items():
            if pos['start'] > end:
                pos['start'] += shift
                pos['end'] += shift
        self.reference_map[method_name]['end'] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, 'w') as f:
            f.write('\n'.join(self.lines) + '\n')
