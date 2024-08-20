# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

__all__ = ["PrimMakerExample"]

from enum import Enum, auto

import omni.kit.commands
import omni.usd
from omni import ui
from omni.kit.ui import EditorMenu
from omni.kit.xr.core import XREditorMenuToggleItem
from omni.kit.xr.scene_view.utils.manipulator_components.area_2d_component import Area2DComponent
from omni.kit.xr.scene_view.utils.manipulator_components.transformable_components import TranslationHandleComponent
from omni.kit.xr.scene_view.utils.manipulator_components.widget_component import WidgetComponent
from omni.kit.xr.scene_view.utils.ui_container import UiContainer
from omni.ui import Menu, color, scene

PRIM_MAKER_EXAMPLE_MENU_PATH: str = "Examples/(XR UI) Prim Maker"
EditorMenuType = Menu | EditorMenu


class PrimType(Enum):
    Cube = auto()
    Cone = auto()
    Cylinder = auto()
    Disk = auto()
    Plane = auto()
    Sphere = auto()
    Torus = auto()


class PrimMakerExampleUI(ui.Widget):
    """
    Essentially a normal omni.ui.Widget subclass.

    This one happens to hook into the currently selected Prim and display
    information about it; but you would be able to put whatever UI display
    code here as needed, almost exactly like you would do for a UI inside
    the Omniverse editor.
    """

    def __init__(self):
        super().__init__()
        self._x_slider_model = ui.SimpleFloatModel(0.0, min=-1000, max=1000)
        self._y_slider_model = ui.SimpleFloatModel(0.0, min=-1000, max=1000)
        self._z_slider_model = ui.SimpleFloatModel(0.0, min=-1000, max=1000)

        # The UI should be built as part of the constructor
        self._build_ui()

    def __del__(self):
        self.destroy()

    def _build_ui(self) -> None:
        """
        Build the omni.ui interface to live inside the scene.
        This is pretty standard-fare omni.ui code, and nothing is being called
        which is specific to using omni.ui.scene within this function.
        """
        self._root_widget = ui.ZStack(style={"padding": 4})
        with self._root_widget:
            ui.Rectangle(style={"background_color": color(0.3), "border_radius": 3})

            with ui.VStack(height=0, spacing=4, style={"margin": 2}):
                with ui.ZStack():
                    omni.ui.Rectangle(style={"background_color": color(0.2), "border_radius": 8})
                    with ui.HStack(width=0, spacing=8):
                        ui.Label("Add Prim to Scene", style={"margin": 6})
                with ui.ZStack(height=0):
                    omni.ui.Rectangle(style={"background_color": color(0.25), "border_radius": 8})
                    with ui.Frame(style={"margin": 4}):
                        with ui.VStack(height=0, spacing=4, style={"margin": 2}):
                            ui.Label("Position:")
                            with ui.HStack(spacing=4):
                                ui.Label("X", width=0)
                                ui.IntSlider(self._x_slider_model, min=-1000, max=1000)
                            with ui.HStack(spacing=4):
                                ui.Label("Y", width=0)
                                ui.IntSlider(self._y_slider_model, min=-1000, max=1000)
                            with ui.HStack(spacing=4):
                                ui.Label("Z", width=0)
                                ui.IntSlider(self._z_slider_model, min=-1000, max=1000)
                            ui.Spacer(height=2)
                            with ui.VStack(style={"margin": 1}):
                                with ui.HStack():
                                    ui.Button(
                                        "Cone",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Cone),
                                    )
                                    ui.Button(
                                        "Cube",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Cube),
                                    )
                                    ui.Button(
                                        "Cylinder",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Cylinder),
                                    )
                                with ui.HStack():
                                    ui.Button(
                                        "Disk",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Disk),
                                    )
                                    ui.Button(
                                        "Plane",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Plane),
                                    )
                                    ui.Button(
                                        "Sphere",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Sphere),
                                    )
                                    ui.Button(
                                        "Torus",
                                        clicked_fn=lambda: self._spawn_prim(PrimType.Torus),
                                    )

    def _spawn_prim(self, prim_type: PrimType) -> None:
        """
        Get the X/Y/Z position from the cached UI slider models and spawn the prim (indicated
        by prim_type) using an Omniverse command.

        Args:
            prim_type: The PrimType value to spawn
        """
        if not self._x_slider_model or not self._y_slider_model or not self._z_slider_model:
            return

        x = self._x_slider_model.as_float
        y = self._y_slider_model.as_float
        z = self._z_slider_model.as_float

        omni.kit.commands.execute(
            "CreateMeshPrimWithDefaultXform",
            prim_type=prim_type.name,
            object_origin=[x, y, z],
        )


class PrimMakerExample:
    def __init__(self, ext_id: str):
        self.example_menu_item = XREditorMenuToggleItem(
            ext_id, PRIM_MAKER_EXAMPLE_MENU_PATH, self._toggle_example, value=False
        )
        self.ui_container: UiContainer[PrimMakerExampleUI] | None = None

    def _toggle_example(self, _menu_path: str, should_show: bool) -> None:
        """
        Toggle the example UI widget visible.

        The UI itself is a standard-fare Omniverse UI, only contained within a
        SceneWidgetManipulator instance (created using the SceneViewUtils factory
        methods).

        Args:
            _menu_path: (Unused) The string-path of the menu being toggled
            should_show: Whether the UI should be shown or hidden
        """
        if should_show:
            widget_component = WidgetComponent(
                PrimMakerExampleUI,
                400,
                248,
                resolution_scale=4.0,
                unit_to_pixel_scale=1.0,
                update_policy=scene.Widget.UpdatePolicy.ALWAYS,
            )
            translate_handle_component = TranslationHandleComponent(width=200, height=16, origin=Area2DComponent.BOTTOM)
            widget_component.add_child(translate_handle_component, Area2DComponent.TOP)

            self.ui_container = UiContainer(widget_component)
        else:
            if self.ui_container:
                self.ui_container.root.clear()
                self.ui_container = None
