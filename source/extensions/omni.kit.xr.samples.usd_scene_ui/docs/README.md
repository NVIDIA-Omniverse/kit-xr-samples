# Kit XR Scene UI Samples [omni.kit.xr.samples.usd_scene_ui]

<p align="left">
  <img src="../data/icon.png" width=15% />
</p>

## Overview

Welcome to the world of Omniverse USD Scene UI Widgets. USD Scene UI provides a functionality to easily bring Omni UI onto a USD Stage. With USD Scene UI, your Omni UI is rendered onto a USD Primitive and placed in your scene to be used in XR or 2d flat.

These samples provide some basic use cases to help you understand how to build your own Scene UI in XR.

## Samples

Anything that can be written with Omni UI can be used in USD Scene UI. The possibilities are only limited by your imagination! Here, we provide four samples to help you get started.

### Basic Widget Gallery
<p align="left">
  <img src="readme-assets/widget_gallery_example.png" width=50% />
</p>

`widget_gallery_example.py`
<br>
<br>
    This example shows 5 basic ways of bringing omni.ui widgets into your scene. Although the omni.ui widgets mostly use
    text, they can be any omni.ui.

    1. Simple static text at the origin.
    2. Camera facing text above the origin.
    3. A counter widget where clicking on the button increases the count.
    4. A text widget parented to a cube. Moving the cube moves the text.
    5. A slider widget that rotates the text above, displaying the yaw degrees.

### Prim Maker
<p align="left">
  <img src="readme-assets/prim_maker_example.png" width=50% />
</p>

`prim_maker_example.py`
<br>
<br>
This example brings up USD Scene UI allowing a user to add a USD primitive at the specified location to the scene when clicking the corresponding primitive type button.

### Prim Transform
<p align="left">
  <img src="readme-assets/prim_transform_example.png" width=50% />
</p>

`prim_transform_example.py`
<br>
<br>
When selecting a prim, this example brings up USD Scene UI which
1. Displays the prim path that is selected.
2. Custom color picker using FloatDrag slider to change the color of the prim path text.
3. Embeds the TransformAttributeWidget used in the Property Window for displaying and altering the selected prim's transform.

### No Code UI with Action Graph
<p align="left">
  <img src="readme-assets/actiongraph_no_code_ui_example.png" width=50% />
</p>

`actiongraph_no_code_ui_example.py`
<br>
<br>
This example shows how to create USD Scene UI purely driven by data. By leveraging the
[No Code UI](https://docs.omniverse.nvidia.com/extensions/latest/ext_no-code-ui.html) and [Action Graph](https://docs.omniverse.nvidia.com/extensions/latest/ext_omnigraph/tutorials/quickstart.html) extensions, you can create USD Scene UI without needing to type a line of code. The python code for this example simply loads a scene having both No Code UI and Action Graphs enabled.
<br>
<br>
Within the scene, the Action Graph handles
1. Displaying camera facing XR Scene UI instructions through No Code UI when loaded.
2. When Pressing 1, attaches text (with an offset in Y) to the cube.
3. When Pressing 2, rotates the cube. If text is attached, the text will rotate as the cube does.
4. When Pressing 3, removes the text from the cube.
<br>
<br>

## License

Development using the Omniverse Kit SDK is subject to the licensing terms detailed [here](https://docs.omniverse.nvidia.com/dev-guide/latest/common/NVIDIA_Omniverse_License_Agreement.html).

## Additional Resources

- [Omniverse Kit SDK Manual](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/index.html)
- [Omniverse Kit App Template](https://github.com/NVIDIA-Omniverse/kit-app-template)


## Contributing

We provide this source code as-is and are currently not accepting outside contributions.