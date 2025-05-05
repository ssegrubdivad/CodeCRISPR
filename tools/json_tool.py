import json

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self._read_file()
        self.reference_map = self._map_keys()

    def _read_file(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _map_keys(self):
        reference_map = {}
        def recurse(obj, path=[]):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    full_path = path + [k]
                    reference_map["::".join(full_path)] = full_path
                    recurse(v, full_path)
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    full_path = path + [str(i)]
                    reference_map["::".join(full_path)] = full_path
                    recurse(v, full_path)
        recurse(self.data)
        return reference_map

    def replace_method(self, key_path, new_value_str):
        if key_path not in self.reference_map:
            raise ValueError(f"Key path '{key_path}' not found.")
        path = self.reference_map[key_path]
        obj = self.data
        for key in path[:-1]:
            obj = obj[key] if not key.isdigit() else obj[int(key)]
        final_key = path[-1]
        new_value = json.loads(new_value_str)
        if final_key.isdigit():
            obj[int(final_key)] = new_value
        else:
            obj[final_key] = new_value

    def save(self, output_path=None):
        path = output_path or self.filepath
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=2)