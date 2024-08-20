# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

__all__ = ["XRSceneViewExampleExtension"]

from typing import Optional

import carb
import omni.ext
import omni.kit.ui

from .actiongraph_no_code_ui_example import ActionGraphNoCodeUiExample
from .prim_maker_example import PrimMakerExample
from .prim_transform_example import PrimTransformExample
from .widget_gallery_example import WidgetGalleryExample


class XRSceneViewExampleExtension(omni.ext.IExt):
    """Creates an extension which will display object info in 3D
    over any object in a UI Scene.
    """

    def __init__(self):
        super().__init__()
        self._ext_id: Optional[str] = None

        self._widget_gallery_example: Optional[WidgetGalleryExample] = None
        self._prim_transform_example: Optional[PrimTransformExample] = None
        self._prim_maker_example: Optional[PrimMakerExample] = None
        self._ag_no_code_ui_example: Optional[ActionGraphNoCodeUiExample] = None

    def on_startup(self, ext_id: str) -> None:
        """Called when the extension is starting up.
        Args:
            ext_id: Extension ID provided by Kit.
        """
        carb.log_info("Sample USD UI scene extension loading")
        self._ext_id = ext_id

        self._widget_gallery_example = WidgetGalleryExample(ext_id)
        self._prim_transform_example = PrimTransformExample(ext_id)
        self._prim_maker_example = PrimMakerExample(ext_id)
        self._ag_no_code_ui_example = ActionGraphNoCodeUiExample(ext_id)

    def on_shutdown(self) -> None:
        """Called when the extension is shutting down."""

        if self._widget_gallery_example:
            self._widget_gallery_example.destroy()
            self._widget_gallery_example = None

        if self._prim_transform_example:
            self._prim_transform_example.destroy()
            self._prim_transform_example = None

        self._prim_maker_example = None

        if self._ag_no_code_ui_example:
            self._ag_no_code_ui_example.destroy()
            self._ag_no_code_ui_example = None
