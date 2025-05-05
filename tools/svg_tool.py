import xml.etree.ElementTree as ET

class CodeCRISPR:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()
        self.reference_map = self._map_elements()

    def _map_elements(self):
        reference_map = {}
        def recurse(elem, path=""):
            tag_id = elem.attrib.get("id")
            display_path = f"{path}/{elem.tag}" if path else elem.tag
            key = f"{display_path}[id={tag_id}]" if tag_id else display_path
            reference_map[key] = elem
            for child in elem:
                recurse(child, display_path)
        recurse(self.root)
        return reference_map

    def replace_method(self, path_key, new_content):
        if path_key not in self.reference_map:
            raise ValueError(f"SVG element path '{path_key}' not found.")
        parent_path = "/".join(path_key.split("/")[:-1])
        tag = path_key.split("/")[-1].split("[")[0]
        parent_elem = None

        for k, v in self.reference_map.items():
            if k.startswith(parent_path) and v.find(tag) is not None:
                parent_elem = v
                break
        else:
            parent_elem = self.root

        new_elem = ET.fromstring(new_content.strip())
        old_elem = self.reference_map[path_key]

        for i, child in enumerate(parent_elem):
            if child is old_elem:
                parent_elem[i] = new_elem
                break

    def save(self, output_path=None):
        path = output_path or self.filepath
        self.tree.write(path, encoding="unicode", xml_declaration=True)