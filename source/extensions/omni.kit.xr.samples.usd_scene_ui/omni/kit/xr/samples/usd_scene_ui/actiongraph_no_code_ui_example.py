# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

__all__ = ["ActionGraphNoCodeUiExample"]

import asyncio

import carb.events
import omni.kit
import omni.kit.window.file
from omni.kit.xr.core import XREditorMenuToggleItem

PRIM_TRANSFORM_EXAMPLE_MENU_PATH: str = "Examples/(XR UI) Action Graph No Code UI"


class ActionGraphNoCodeUiExample:
    """
    Example showing how to incorporate Action Graph, No Code UI (Data Driven UI) with XR Scene UI.
    Documentation on No Code UI can be found at: https://docs.omniverse.nvidia.com/extensions/latest/ext_no-code-ui.html

    The example simply loads the scene 'no_code_ag_example.usd', which contains all the necessary logic an Action Graph that:
        * Displays camera facing XR Scene UI instructions through No Code UI when loaded.
        * When Pressing 1, attaches text (with an offset in Y) to the cube.
        * When Pressing 2, rotates the cube. If text is attached, the text will rotate as the cube does.
        * When Pressing 3, removes the text from the cube.
    """

    def __init__(self, ext_id: str):
        self._ext_id = ext_id
        self._example_menu_item = XREditorMenuToggleItem(
            self._ext_id, PRIM_TRANSFORM_EXAMPLE_MENU_PATH, self._toggle_example, value=False
        )

    def _toggle_example(self, _menu_path: str, should_show: bool) -> None:
        if should_show:

            async def __load_scene():
                # Wait a frame to allow any save prompts to be destroyed.
                # Work around to an issue with opening a stage in the same frame as destroying the prompt.
                await omni.kit.app.get_app().next_update_async()

                extension_path = omni.kit.app.get_app().get_extension_manager().get_extension_path(self._ext_id)
                scene_path = extension_path + "/data/examples/no_code_ag_example.usd"
                omni.usd.get_context().open_stage(scene_path)

                self._example_menu_item.ticked_value = True

            self._example_menu_item.ticked_value = False
            omni.kit.window.file.prompt_if_unsaved_stage(lambda *_: asyncio.ensure_future(__load_scene()))

    def destroy(self):
        self._example_menu_item = None
