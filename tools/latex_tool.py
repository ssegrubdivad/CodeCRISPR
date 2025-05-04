import re

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file()
        self.reference_map = self._parse_environments()

    def _read_file(self):
        with open(self.filepath, 'r') as f:
            return f.read().splitlines()

    def _parse_environments(self):
        pattern = re.compile(r'^\\s*\\\\begin\\{(\\w+)\\}')
        reference_map = {}
        i = 0
        while i < len(self.lines):
            match = pattern.match(self.lines[i])
            if match:
                env = match.group(1)
                start = i
                while i < len(self.lines):
                    if re.match(r'^\\s*\\\\end\\{%s\\}' % re.escape(env), self.lines[i]):
                        break
                    i += 1
                end = i
                key = f"{env}_{start}"
                reference_map[key] = {'start': start, 'end': end}
            i += 1
        return reference_map

    def replace_method(self, name, new_code):
        if name not in self.reference_map:
            raise ValueError(f"LaTeX environment block '{name}' not found.")
        start = self.reference_map[name]['start']
        end = self.reference_map[name]['end']
        new_lines = new_code.strip('\\n').splitlines()
        self.lines[start:end + 1] = new_lines
        shift = len(new_lines) - (end - start + 1)
        for k, bounds in self.reference_map.items():
            if bounds['start'] > end:
                bounds['start'] += shift
                bounds['end'] += shift
        self.reference_map[name]['end'] = start + len(new_lines) - 1

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, 'w') as f:
            f.write('\\n'.join(self.lines) + '\\n')