import re

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_functions()

    def _read_file(self):
        with open(self.filepath, 'r') as f:
            return f.read().splitlines()

    def _parse_functions(self):
        # Enhanced patterns for Rust functions and methods
        patterns = [
            # Free functions (async, const, pub, etc.)
            re.compile(r"^\s*(?:pub(?:\(.*?\))?\s+)?(?:async\s+)?(?:const\s+)?(?:unsafe\s+)?fn\s+(\w+)\s*(?:<.*?>)?\s*\(.*?\)(?:\s*->\s*[^{]+)?\s*\{"),
            # Methods in impl blocks
            re.compile(r"^\s*(?:pub(?:\(.*?\))?\s+)?(?:async\s+)?(?:const\s+)?(?:unsafe\s+)?fn\s+(\w+)\s*(?:<.*?>)?\s*\(.*?\)(?:\s*->\s*[^{]+)?\s*\{"),
        ]
        
        reference_map = {}
        i = 0
        in_impl = False
        impl_type = ""
        
        while i < len(self.lines):
            line = self.lines[i]
            
            # Track impl blocks
            impl_match = re.match(r"^\s*impl(?:<.*?>)?\s+(?:(\w+)\s+for\s+)?(\w+)", line)
            if impl_match:
                in_impl = True
                impl_type = impl_match.group(2)
                i += 1
                continue
            
            # Check if leaving impl block
            if in_impl and line.strip() == "}" and self.lines[i-1].strip() != "}":
                in_impl = False
                impl_type = ""
            
            # Match functions
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    name = match.group(1)
                    # If in impl block, prefix with type name
                    if in_impl and impl_type:
                        name = f"{impl_type}::{name}"
                    
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
                    i = end + 1
                    break
            else:
                i += 1
        
        return reference_map
    def replace_method(self, name, new_code):
        if name not in self.reference_map:
            raise ValueError(f"Rust function '{name}' not found.")
        start = self.reference_map[name]['start']
        end = self.reference_map[name]['end']
        new_lines = new_code.strip('\n').splitlines()
        self.lines[start:end + 1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for k, v in self.reference_map.items():
            if v['start'] > end:
                v['start'] += shift
                v['end'] += shift
        self.reference_map[name]['end'] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, "w") as f:
            f.write("\n".join(self.lines) + "\n")
