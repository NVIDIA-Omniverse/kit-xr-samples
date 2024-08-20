# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

__all__ = ["PrimTransformExample"]

import weakref

import carb.events
import omni
import omni.kit.app as app
from carb.events import ISubscription
from omni import ui
from omni.kit.property.transform.scripts.transform_widget import TransformAttributeWidget
from omni.kit.property.usd.prim_selection_payload import PrimSelectionPayload
from omni.kit.xr.core import XREditorMenuToggleItem
from omni.kit.xr.scene_view.utils import UiContainer, WidgetComponent
from omni.kit.xr.scene_view.utils.spatial_source import SpatialSource
from omni.ui import color as cl
from omni.ui import scene
from pxr import Gf, Sdf, Usd, UsdGeom

PRIM_TRANSFORM_EXAMPLE_MENU_PATH: str = "Examples/(XR UI) Prim Transform"
NOTHING_SELECTED_TEXT = "...no prim selected..."
# The distance to raise above the top of the object's bounding box
TOP_OFFSET = 150


class PrimInfoWidget(ui.Widget):
    """
    This widget contains:
    * Simple text displaying the prim path that is selected.
    * Custom color picker using FloatDrag items to change the color of the prim text.
    * TransformAttributeWidget that is used in the Property Window for altering the selected prim's transform.
    """

    def __init__(self, sdf_path: Sdf.Path, **kwargs):
        super().__init__(**kwargs)

        self._selected_sdf_path = sdf_path
        self._prim_name_label: ui.Label | None = None

        self._red_model = ui.SimpleFloatModel(1.0)
        self._green_model = ui.SimpleFloatModel(1.0)
        self._blue_model = ui.SimpleFloatModel(1.0)

        self._red_model.add_value_changed_fn(self._label_color_value_changed)
        self._green_model.add_value_changed_fn(self._label_color_value_changed)
        self._blue_model.add_value_changed_fn(self._label_color_value_changed)

        self._build_ui()

    def __del__(self):
        self._prim_name_label = None
        self._transform_widget = None
        self.destroy()

    def _build_ui(self):
        with ui.ZStack():
            ui.Rectangle(style={"Rectangle": {"background_color": 0xFF454545, "border_radius": 3}})

            with ui.VStack():
                # Create the Prim Path Label.
                with ui.HStack(height=20):
                    ui.Label("Prim Path", width=70)
                    with ui.ZStack():
                        ui.Rectangle(style={"Rectangle": {"background_color": 0xFF222222}})
                        self._prim_name_label = ui.Label(
                            str(self._selected_sdf_path),
                            alignment=ui.Alignment.LEFT_CENTER,
                        )

                # Create a custom color picker for the Prim Path Label.
                with ui.HStack(height=20):
                    ui.Label("Label Color", width=0)
                    ui.Spacer(width=9)

                    with ui.ZStack(width=12):
                        ui.Rectangle(style={"Rectangle": {"background_color": 0xFF5555AA}})
                        ui.Label("R", alignment=ui.Alignment.CENTER)
                    ui.FloatDrag(self._red_model, min=0.0, max=1.0)

                    with ui.ZStack(width=12):
                        ui.Rectangle(style={"Rectangle": {"background_color": 0xFF71A376}})
                        ui.Label("G", alignment=ui.Alignment.CENTER)
                    ui.FloatDrag(self._green_model, min=0.0, max=1.0)

                    with ui.ZStack(width=12):
                        ui.Rectangle(style={"Rectangle": {"background_color": 0xFFA07D4F}})
                        ui.Label("B", alignment=ui.Alignment.CENTER)
                    ui.FloatDrag(self._blue_model, min=0.0, max=1.0)

                # Create a Transform Widget for the selected Prim. This is the same widget that is used in the Property Window.
                stage = omni.usd.get_context().get_stage()
                payload = PrimSelectionPayload(weakref.ref(stage), [self._selected_sdf_path])

                self._transform_widget = TransformAttributeWidget(title="Transform", collapsed=False)
                if self._transform_widget.on_new_payload(payload):
                    self._transform_widget.build()

    def _label_color_value_changed(self, _: ui.AbstractValueModel):
        new_color = cl(
            self._red_model.as_float,
            self._green_model.as_float,
            self._blue_model.as_float,
            1.0,
        )
        if not self._prim_name_label:
            raise ValueError(f"{self._prim_name_label=}")
        self._prim_name_label.style = {"color": new_color}


class PrimTransformExample:
    """
    This example shows how one can attach camera facing scene ui to the selected prim.
    """

    def __init__(self, ext_id: str):
        self._example_menu_item = XREditorMenuToggleItem(
            ext_id, PRIM_TRANSFORM_EXAMPLE_MENU_PATH, self._toggle_example, value=False
        )

        self._widget_container: UiContainer[PrimInfoWidget] | None = None
        self._selected_prim: Usd.Prim | None = None
        self._stage_event_delegate: ISubscription | None = None

    def destroy(self):
        self._hide()
        self._example_menu_item = None

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

    def _show(self):
        self._usd_context = omni.usd.get_context()
        self._stage_event_delegate = self._usd_context.get_stage_event_stream().create_subscription_to_pop(
            self._on_stage_event,
            name="Stage event updates for Prim Info UI Example",
        )

        selected_paths = self._usd_context.get_selection().get_selected_prim_paths()
        if len(selected_paths) > 0:
            self._on_prim_selection_changed(Sdf.Path(selected_paths[0]))

    def _hide(self):
        self._app_update_sub = None

        if self._stage_event_delegate:
            self._stage_event_delegate.unsubscribe()

        if self._widget_container:
            self._widget_container.root.clear()
            self._widget_container = None

    def _on_stage_event(self, event) -> None:
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            selected_paths = self._usd_context.get_selection().get_selected_prim_paths()
            path = Sdf.Path(selected_paths[0]) if len(selected_paths) > 0 else None
            self._on_prim_selection_changed(path)

    def _on_prim_selection_changed(self, prim_path: Sdf.Path) -> None:
        if str(self._selected_prim) == prim_path:
            return

        if self._widget_container:
            self._widget_container.root.clear()
            self._widget_container = None

        self._selected_prim = None

        if not prim_path:
            return

        # # Handle bug where UI is selectable.
        # if str(prim_path).startswith("/ui/"):
        #     return

        prim = self._usd_context.get_stage().GetPrimAtPath(prim_path)
        if not UsdGeom.Xformable(prim):
            return

        self._selected_prim = prim

        # We want to put the widget above the bounding box of the prim so it doesn't get obstructed.
        box_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])
        bound = box_cache.ComputeWorldBound(self._selected_prim)
        range = bound.ComputeAlignedBox()
        bboxMax = range.GetMax()

        # Find the top center of the bounding box and add a small offset upward.
        top_offset = bboxMax[1] + TOP_OFFSET

        widget_component = WidgetComponent(
            PrimInfoWidget,
            300,
            150,
            3,
            widget_kwargs={"sdf_path": prim_path},
            update_policy=scene.Widget.UpdatePolicy.ALWAYS,
        )

        self._widget_container = UiContainer(
            widget_component,
            # Optional SpatialSources. If these are removed, the widget will be at static at origin.
            space_stack=[
                # Parent the widget to the prim_path.
                SpatialSource.new_prim_path_source(str(prim_path)),
                # Make the widget camera facing.
                SpatialSource.new_look_at_camera_source(),
                # Set the widget above the prim so that the widget is not obstructed by the prim.
                SpatialSource.new_translation_source(Gf.Vec3d(0, top_offset, 0)),
            ],
        )
