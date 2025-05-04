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
        # Enhanced patterns for Python functions and methods
        patterns = [
            # Regular and async functions
            re.compile(r"^\s*(async\s+)?def\s+(\w+)\s*\(.*?\):"),
            # Class methods with decorators (staticmethod, classmethod, property)
            re.compile(r"^\s*@(staticmethod|classmethod|property)\s*$"),
            # Custom decorators
            re.compile(r"^\s*@\w+(?:\.\w+)*(?:\(.*?\))?\s*$"),
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
            elif in_class and line.strip() and len(line) - len(line.lstrip()) <= class_indent:
                if not re.match(r"^\s*def\s+", line) and not re.match(r"^\s*@", line):
                    in_class = False
            
            # Check for decorators
            decorator_lines = []
            original_i = i
            while i < len(self.lines) and re.match(r"^\s*@", self.lines[i]):
                decorator_lines.append(i)
                i += 1
            
            # Check for function definition after decorators
            if i < len(self.lines):
                match = re.match(r"^\s*(async\s+)?def\s+(\w+)\s*\(.*?\):", self.lines[i])
                if match:
                    name = match.group(2)
                    start = decorator_lines[0] if decorator_lines else i
                    indent = len(self.lines[i]) - len(self.lines[i].lstrip())
                    j = i + 1
                    
                    # Find the end of the function
                    while j < len(self.lines):
                        line = self.lines[j]
                        if line.strip() == "":
                            j += 1
                            continue
                        line_indent = len(line) - len(line.lstrip())
                        if line_indent <= indent:
                            break
                        j += 1
                    
                    end = j - 1
                    reference_map[name] = {"start": start, "end": end}
                    i = j
                else:
                    i = original_i + 1
            else:
                i = original_i + 1
        
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
            if pos['start'] > end:
                pos['start'] += shift
                pos['end'] += shift
        self.reference_map[method_name]["end"] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, 'w') as f:
            f.write('\n'.join(self.lines) + '\n')
