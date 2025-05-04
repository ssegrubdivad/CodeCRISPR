import re

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_div_blocks()

    def _read_file(self):
        with open(self.filepath, 'r') as f:
            return f.read().splitlines()

    def _parse_div_blocks(self):
        pattern = re.compile(r'^\s*<div\s+id="([^"]+)".*?>')
        reference_map = {}
        i = 0
        while i < len(self.lines):
            match = pattern.match(self.lines[i])
            if match:
                name = match.group(1)
                start = i
                depth = 1
                i += 1
                while i < len(self.lines):
                    if "<div" in self.lines[i]:
                        depth += 1
                    if "</div>" in self.lines[i]:
                        depth -= 1
                    if depth == 0:
                        break
                    i += 1
                end = i
                reference_map[name] = {"start": start, "end": end}
            else:
                i += 1
        return reference_map

    def replace_method(self, block_id, new_code):
        if block_id not in self.reference_map:
            raise ValueError(f"<div id='{block_id}'> block not found.")
        start = self.reference_map[block_id]["start"]
        end = self.reference_map[block_id]["end"]
        new_lines = new_code.strip("\n").splitlines()
        self.lines[start:end+1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for k, v in self.reference_map.items():
            if v["start"] > end:
                v["start"] += shift
                v["end"] += shift
        self.reference_map[block_id]["end"] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, "w") as f:
            f.write("\n".join(self.lines) + "\n")