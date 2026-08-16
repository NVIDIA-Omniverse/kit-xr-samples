import ast
import os
import unittest


class TestActionGraphImport(unittest.TestCase):
    def test_omni_usd_is_imported(self):
        module_path = os.path.join(
            os.path.dirname(__file__), "..", "omni", "kit", "xr", "samples", "usd_scene_ui",
            "actiongraph_no_code_ui_example.py",
        )
        with open(module_path, "r", encoding="utf-8") as f:
            source = f.read()
        imports = {
            alias.name
            for node in ast.walk(ast.parse(source))
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertIn("omni.usd", imports)

