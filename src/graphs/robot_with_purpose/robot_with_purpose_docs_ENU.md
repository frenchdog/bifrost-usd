## `Robot with Purpose Example`

A USD Prim can have different purpose, from being used as a proxy representation to only be visible at render time.
You can find more information on [Purpose concept in the USD glossary](https://graphics.pixar.com/usd/release/glossary.html#usdglossary-purpose)

For example, the mayaUSDProxyShape allows you to toggle purpose categories on and off (in the Attribute Editor) to change their visibility in the Viewport.
Note: These checkboxes can work simultaneously. For example, Proxy and Guide can both be toggled on.

### What it does

This graph takes an array of Bifrost meshes used to construct three different representations of the robot.
Note that in this example the Bifrost meshes are created from a USD file by using the _read_usd_meshes_ compound,
but you could also (for example) select several Maya meshes and drag and drop them in the Bifrost Graph Editor as
a starting point.

### Guide purpose

In the *define_guides_prims* compound, for each Bifrost mesh, define a USD Capsule matching its bounding box.
Those new prim definitions are connected to the children of a define_usd_prim compound "/guides" with its Purpose parameter set to *Guide*.

### Proxy purpose

In the *define_proxy_prims* compound, for each Bifrost mesh, define a USD Cube matching its bounding box.
Those new prim definitions are connected to the children of a define_usd_prim compound "/proxies" with its Purpose parameter set to *Proxy*.

### Render purpose

In the *define_render_prims* compound, the original USD layer is referenced under the "/render/Robot" prim.
The "/renders" prim Purpose parameter is set to *Render*.
