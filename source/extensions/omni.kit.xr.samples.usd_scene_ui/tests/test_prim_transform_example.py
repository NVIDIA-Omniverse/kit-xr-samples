import sys
import unittest
from unittest.mock import MagicMock

sys.modules["omni"] = MagicMock()
sys.modules["omni.kit"] = MagicMock()
sys.modules["omni.kit.app"] = MagicMock()
sys.modules["omni.usd"] = MagicMock()
sys.modules["carb"] = MagicMock()
sys.modules["carb.events"] = MagicMock()
sys.modules["omni.ui"] = MagicMock()
sys.modules["omni.kit.property.transform.scripts.transform_widget"] = MagicMock()
sys.modules["omni.kit.property.usd.prim_selection_payload"] = MagicMock()
sys.modules["omni.kit.xr.core"] = MagicMock()
sys.modules["omni.kit.xr.scene_view.utils"] = MagicMock()
sys.modules["omni.kit.xr.scene_view.utils.spatial_source"] = MagicMock()
sys.modules["pxr"] = MagicMock()
sys.modules["pxr.Gf"] = MagicMock()
sys.modules["pxr.Sdf"] = MagicMock()
sys.modules["pxr.Usd"] = MagicMock()
sys.modules["pxr.UsdGeom"] = MagicMock()

from omni.kit.xr.samples.usd_scene_ui.prim_transform_example import PrimTransformExample


class TestPrimTransformExample(unittest.TestCase):
    def test_hide_clears_stage_event_delegate(self):
        """_hide must reset the delegate reference after unsubscribing."""
        example = PrimTransformExample("ext_id")
        mock_delegate = MagicMock()
        example._stage_event_delegate = mock_delegate
        example._widget_container = None
        example._usd_context = None

        example._hide()

        mock_delegate.unsubscribe.assert_called_once()
        self.assertIsNone(example._stage_event_delegate)


if __name__ == "__main__":
    unittest.main()
