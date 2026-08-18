import importlib
import inspect
import unittest
from unittest.mock import MagicMock


class TestExtensionShutdown(unittest.TestCase):
    def test_prim_maker_example_is_destroyed(self):
        module = importlib.import_module("omni.kit.xr.samples.usd_scene_ui.extension")
        ext_classes = [
            obj
            for obj in module.__dict__.values()
            if inspect.isclass(obj)
            and obj.__module__ == module.__name__
            and hasattr(obj, "on_shutdown")
        ]
        self.assertTrue(ext_classes, "extension class with on_shutdown not found")

        ext = ext_classes[0]()
        ext._prim_transform_example = None
        ext._prim_maker_example = MagicMock()
        ext._ag_no_code_ui_example = None

        ext.on_shutdown()

        ext._prim_maker_example.destroy.assert_called_once()
        self.assertIsNone(ext._prim_maker_example)


if __name__ == "__main__":
    unittest.main()
