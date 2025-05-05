import re

class MethodEditor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_sections()

    def _read_file(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.read().splitlines()

    def _parse_sections(self):
        reference_map = {}
        pattern = re.compile(r'^(#+)\s+(.*\S.*?)\s*$')
        headings = []

        for i, line in enumerate(self.lines):
            match = pattern.match(line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((title, level, i))

        for idx, (title, level, start) in enumerate(headings):
            if idx + 1 < len(headings):
                next_start = headings[idx + 1][2]
                end = next_start - 1
            else:
                end = len(self.lines) - 1
            reference_map[title] = {'start': start, 'end': end}

        return reference_map

    def replace_method(self, section_title, new_code):
        if section_title not in self.reference_map:
            raise ValueError(f"Section heading '{section_title}' not found.")
        start = self.reference_map[section_title]['start']
        end = self.reference_map[section_title]['end']
        new_lines = new_code.strip('\n').splitlines()
        self.lines[start:end + 1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for k, v in self.reference_map.items():
            if v['start'] > end:
                v['start'] += shift
                v['end'] += shift
        self.reference_map[section_title]['end'] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")