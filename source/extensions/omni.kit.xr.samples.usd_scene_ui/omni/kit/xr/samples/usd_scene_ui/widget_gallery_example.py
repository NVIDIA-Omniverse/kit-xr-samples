# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import asyncio
import math
from typing import Any, Callable, Dict, Optional

import omni.kit.commands
from omni import ui
from omni.kit.xr.core import XREditorMenuToggleItem
from omni.kit.xr.scene_view.utils import UiContainer, WidgetComponent
from omni.kit.xr.scene_view.utils.spatial_source import RotationSpace, SpatialSource
from omni.ui import scene
from pxr import Gf

WIDGET_GALLERY_EXAMPLE_MENU_PATH: str = "Examples/(XR UI) Basic Widget Gallery"


class SimpleTextWidget(ui.Widget):
    def __init__(self, text: Optional[str] = "Simple Text", style: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)

        if style is None:
            style = {"font_size": 50}

        self._ui_label: Optional[ui.Label] = None
        self._text = text
        self._style = style
        self._build_ui()

    def set_label_text(self, text: str):
        self._text = text
        if self._ui_label:
            self._ui_label.text = self._text

    def _build_ui(self):
        self._ui_label = ui.Label(self._text, style=self._style, alignment=ui.Alignment.CENTER)


class SliderWidget(ui.Widget):
    def __init__(self, min: float, max: float, callback: Callable[[ui.AbstractValueModel], None], **kwargs):
        super().__init__(**kwargs)

        self._slider_model = ui.SimpleFloatModel(0.0)
        self._slider_model.add_value_changed_fn(callback)

        ui.FloatDrag(self._slider_model, min=min, max=max)


class CountingWidget(ui.Widget):
    """
    This counting widget adds 1 to the text everytime the button is pressed.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ui_label: Optional[ui.Label] = None
        self._ui_button: Optional[ui.Button] = None

        self._count = 0
        self._text = str(self._count)
        self._build_ui()

    def set_label_text(self, text: str):
        self._text = text
        if hasattr(self, "_ui_label"):
            self._ui_label.text = self._text

    def _on_button_clicked(self):
        self._count = self._count + 1
        self._ui_label.text = str(self._count)

    def _build_ui(self):
        with ui.VStack():
            self._ui_label = ui.Label(self._text, style={"font_size": 100}, alignment=ui.Alignment.CENTER)
            self._ui_button = ui.Button("Add 1", style={"font_size": 50}, clicked_fn=self._on_button_clicked)


class WidgetGalleryExample:
    """
    This example shows 5 basic ways of bringing omni.ui widgets into your scene. Although the omni.ui widgets mostly use
    text, they can be any omni.ui.

    1. Simple static text at the origin.
    2. Camera facing text above the origin.
    3. A counter widget where clicking on the button increases the count.
    4. A text widget parented to a cube. Moving the cube moves the text.
    5. A slider widget that rotates the text above, displaying the yaw degrees.
    """

    def __init__(self, ext_id: str):
        self._static_text_widget_container: Optional[UiContainer] = None
        self._camera_facing_widget_container: Optional[UiContainer] = None
        self._counting_widget_container: Optional[UiContainer] = None
        self._parented_widget_container: Optional[UiContainer] = None
        self._rotatable_text_widget_container: Optional[UiContainer] = None
        self._rotatable_slider_widget_container: Optional[UiContainer] = None

        self._example_menu_item = XREditorMenuToggleItem(
            ext_id, WIDGET_GALLERY_EXAMPLE_MENU_PATH, self._toggle_example, value=False
        )

    def destroy(self):
        self._hide()

    def _toggle_example(self, _menu_path: str, should_show: bool) -> None:
        """
        Toggle the example UI widget visible.

        Args:
            _menu_path: (Unused) The string-path of the menu being toggled
            should_show: Whether the UI should be shown or hidden
        """
        if should_show:
            self._show()
        else:
            self._hide()

    def _hide(self):
        if self._static_text_widget_container:
            self._static_text_widget_container.root.clear()
            self._static_text_widget_container = None

        if self._camera_facing_widget_container:
            self._camera_facing_widget_container.root.clear()
            self._camera_facing_widget_container = None

        if self._counting_widget_container:
            self._counting_widget_container.root.clear()
            self._counting_widget_container = None

        if self._parented_widget_container:
            self._parented_widget_container.root.clear()
            self._parented_widget_container = None

        if self._rotatable_text_widget_container:
            self._rotatable_text_widget_container.root.clear()
            self._rotatable_text_widget_container = None

        if self._rotatable_slider_widget_container:
            self._rotatable_slider_widget_container.root.clear()
            self._rotatable_slider_widget_container = None

    def _show(self):
        # 1. Place static "Simple Text" at the origin.
        static_text_widget_component = WidgetComponent(SimpleTextWidget, width=400, height=200)

        self._static_text_widget_container = UiContainer(static_text_widget_component)

        # 2. Camera facing widget 200 units above the Static Label.
        # Increase the resolution_scale. Notice that the text appears sharper.
        camera_facing_widget_component = WidgetComponent(
            SimpleTextWidget,
            width=400,
            height=200,
            resolution_scale=2,
            widget_args=["Camera Facing", {"font_size": 50, "color": omni.ui.color.green}],
        )

        self._camera_facing_widget_container = UiContainer(
            camera_facing_widget_component,
            space_stack=[
                SpatialSource.new_translation_source(Gf.Vec3d(0, 200, 0)),
                SpatialSource.new_look_at_camera_source(),
            ],
        )

        # 3. A counting widget to the left of the static widget and rotated 45 degrees in yaw to face the user.
        counting_widget_component = WidgetComponent(CountingWidget, width=200, height=200, resolution_scale=2)

        self._counting_widget_container = UiContainer(
            counting_widget_component,
            space_stack=[
                SpatialSource.new_translation_source(Gf.Vec3d(-600, 100, 0)),
                SpatialSource.new_rotation_source(Gf.Vec3d(0, 45, 0)),
            ],
        )

        # 4. Create a Cube and place a text widget parented above it.
        _, cube_prim_path = omni.kit.commands.execute(
            "CreateMeshPrimWithDefaultXform", prim_type="Cube", object_origin=[400, 0, 0], select_new_prim=False
        )

        async def __wait_one_frame():
            # Wait one frame after creating the Cube as it is not ready.
            await omni.kit.app.get_app().next_update_async()

            parented_widget_component = WidgetComponent(
                SimpleTextWidget, width=400, height=200, resolution_scale=2, widget_args=["Parented to Cube"]
            )

            self._parented_widget_container = UiContainer(
                parented_widget_component,
                space_stack=[
                    SpatialSource.new_prim_path_source(cube_prim_path),
                    SpatialSource.new_translation_source(Gf.Vec3d(0, 100, 0)),
                ],
            )

        asyncio.ensure_future(__wait_one_frame())

        # Create two widgets, one text and one slider. The slider causes the text to rotate.
        # We don't want to create both in a single omni.ui widget because if we don't want to rotate the slider.
        # Both rotated 45 degrees in yaw to face the user.
        rotatable_text_widget_component = WidgetComponent(
            SimpleTextWidget, width=400, height=200, resolution_scale=2, widget_args=["Slide to rotate"]
        )

        self._rotation_source = SpatialSource.new_rotation_source(Gf.Vec3d(0, 45, 0))
        self._rotatable_text_widget_container = UiContainer(
            rotatable_text_widget_component,
            space_stack=[SpatialSource.new_translation_source(Gf.Vec3d(-600, 350, 0)), self._rotation_source],
        )

        def __on_rotate(value: ui.AbstractValueModel):
            # Since we start at a 45 degree offset, include it here.
            degrees = (value.as_float * 180.0) + 45.0
            radians = math.radians(degrees)
            self._rotation_source.source = RotationSpace(Gf.Vec3d(0, radians, 0))
            rotatable_text_widget_component.widget.set_label_text(f"{degrees:.2f}")

        rotatable_slider_widget_component = WidgetComponent(
            SliderWidget, width=200, height=200, resolution_scale=2, widget_args=[-1.0, 1.0, __on_rotate]
        )

        self._rotatable_slider_widget_container = UiContainer(
            rotatable_slider_widget_component,
            space_stack=[
                SpatialSource.new_translation_source(Gf.Vec3d(-600, 200, 0)),
                SpatialSource.new_rotation_source(Gf.Vec3d(0, 45, 0)),
            ],
        )
