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
            tag_path = f"{path}/{elem.tag}" if path else elem.tag
            reference_map[tag_path] = elem
            for child in elem:
                recurse(child, tag_path)
        recurse(self.root)
        return reference_map

    def replace_method(self, tag_path, new_content):
        if tag_path not in self.reference_map:
            raise ValueError(f"XML tag path '{tag_path}' not found.")
        parent_path = '/'.join(tag_path.split('/')[:-1])
        tag_name = tag_path.split('/')[-1]
        parent_elem = self.reference_map.get(parent_path, self.root)

        new_elem = ET.fromstring(new_content.strip())
        for i, child in enumerate(parent_elem):
            if child.tag == tag_name:
                parent_elem[i] = new_elem
                break

    def save(self, output_path=None):
        path = output_path or self.filepath
        self.tree.write(path, encoding='unicode', xml_declaration=True)