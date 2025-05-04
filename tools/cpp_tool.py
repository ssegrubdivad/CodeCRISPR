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
        # Enhanced patterns for C++ functions and methods
        patterns = [
            # Class methods (ClassName::methodName)
            re.compile(r'^\s*(?:[\w:*&<>]+\s+)+(\w+)::(\w+)\s*\(.*?\)(?:\s*const)?(?:\s*override)?(?:\s*final)?(?:\s*noexcept(?:\(.*?\))?)?\s*\{'),
            # Free functions (including templates, inline, constexpr)
            re.compile(r'^\s*(?:template\s*<.*?>\s*)?(?:inline\s+)?(?:constexpr\s+)?(?:static\s+)?(?:[\w:*&<>]+\s+)+(\w+)\s*\(.*?\)(?:\s*const)?(?:\s*noexcept(?:\(.*?\))?)?\s*\{'),
            # Constructors and destructors
            re.compile(r'^\s*(?:explicit\s+)?(\w+)\s*\(.*?\)(?:\s*:\s*.*?)?\s*\{'),
            re.compile(r'^\s*~(\w+)\s*\(\s*\)(?:\s*noexcept)?\s*\{'),
        ]
        
        reference_map = {}
        i = 0
        
        while i < len(self.lines):
            line = self.lines[i]
            
            # Skip preprocessor directives
            if line.strip().startswith('#'):
                i += 1
                continue
            
            # Match functions and methods
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    if pattern == patterns[0]:  # Class method
                        class_name = match.group(1)
                        method_name = match.group(2)
                        name = f"{class_name}::{method_name}"
                    else:  # Free function or constructor/destructor
                        name = match.group(1)
                    
                    start = i
                    brace_count = 0
                    j = i
                    
                    # Count braces to find the end
                    while j < len(self.lines):
                        # Skip string literals and comments
                        clean_line = re.sub(r'".*?"|\'.*?\'|//.*$|/\*.*?\*/', '', self.lines[j])
                        brace_count += clean_line.count('{')
                        brace_count -= clean_line.count('}')
                        if brace_count == 0 and j > i:
                            break
                        j += 1
                    
                    end = j
                    reference_map[name] = {'start': start, 'end': end}
                    i = end + 1
                    break
            else:
                i += 1
        
        return reference_map

    def replace_method(self, method_name, new_code):
        if method_name not in self.reference_map:
            raise ValueError(f"C++ method '{method_name}' not found.")
        start = self.reference_map[method_name]["start"]
        end = self.reference_map[method_name]["end"]
        new_lines = new_code.strip("\n").splitlines()
        self.lines[start:end + 1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for k, v in self.reference_map.items():
            if v["start"] > end:
                v["start"] += shift
                v["end"] += shift
        self.reference_map[method_name]["end"] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, "w") as f:
            f.write("\n".join(self.lines) + "\n")