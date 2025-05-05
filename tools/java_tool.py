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
        pattern = re.compile(r'^\s*(public|private|protected)?\s*(static\s+)?(final\s+)?[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*(throws\s+[\w,\s]+)?\s*\{')
        reference_map = {}
        i = 0
        while i < len(self.lines):
            match = pattern.match(self.lines[i])
            if match:
                name = match.group(4)
                start = i
                brace_count = 0
                j = i
                while j < len(self.lines):
                    line = re.sub(r'"[^"]*"|//.*|/\*.*?\*/', '', self.lines[j])
                    brace_count += line.count('{')
                    brace_count -= line.count('}')
                    if brace_count == 0 and j > i:
                        break
                    j += 1
                end = j
                reference_map[name] = {'start': start, 'end': end}
                i = end + 1
            else:
                i += 1
        return reference_map

    def replace_method(self, method_name, new_code):
        if method_name not in self.reference_map:
            raise ValueError(f"Java method '{method_name}' not found.")
        start = self.reference_map[method_name]["start"]
        end = self.reference_map[method_name]["end"]
        new_lines = new_code.strip("\n").splitlines()
        self.lines[start:end+1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for name, bounds in self.reference_map.items():
            if bounds["start"] > end:
                bounds["start"] += shift
                bounds["end"] += shift
        self.reference_map[method_name]["end"] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, "w") as f:
            f.write("\n".join(self.lines) + "\n")