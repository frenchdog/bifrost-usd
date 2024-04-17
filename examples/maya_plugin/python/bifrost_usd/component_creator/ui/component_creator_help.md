# What is a Component?
A _Component_ is the smallest reference-able USD Model. It can be referenced "as is" in an other stage, or can be combined (with other components) into an _Assembly_ Model that can also be referenced in an other stage.
```

```
## Component Creator
Creates a Bifrost Graph with a _create_usd_component_ compound. The graph result is a stage with the following features:
- A default prim using the _Model Name_
- A _payload_ layer to load the asset only if needed.
- (optional) A _Model_ VariantSet to select different modeling variants from the default prim.
- (optional) A _Look_ VariantSet to select different look variants from the default prim.
- The _extentsHint_ attributes to display the component as a bounding box added on the default prim.
- The _assetInfo_ metadata
- A _Bifrost::usd_component_ dictionnary (in customLayerData) storing information like the host scene who generated the component.

```

```
### To Create a USD Component
1. Choose **Bifrost USD > Create > Component Creator** from the Bifrost USD menu.
2. In dialog that appear, browse to a component root directory.
3. If the component is versionned, select a version.
4. Click **Ok**
```

```
## The component directory structure
* The component root directory must use the component name.
* A *geo* or *Geometries* subdirectory must contain one or several USD files.
```

```
Example:
```
	Shuttle                    <- Component root directory
	|_ geo                     <- geometries directory
	  |_ default.usd           <- The default geometry layer

```
### You can have more than one geometry file.

The _Component Creator_ will use them to create model variants and/or guide/proxy/render purposes.
To automatically create variants and purposes, the following naming convention must be used for the files:
   `<variant name>_<purpose name>.usd`.
```

```
Example:
```
	Shuttle <- Component root directory
	|_ geo  <- geometries directory
	  |_ small_proxy.usd    <- The proxy geometries for the small shuttle variant.
	  |_ small_render.usd   <- The render geometries for the small shuttle variant.
	  |_ tall_proxy.usd     <- The proxy geometries for the tall shuttle variant.
	  |_ tall_render.usd    <- The render geometries for the tall shuttle variant.

```
You can use a different naming convention fitting your pipeline, but in this case the _Component Creator_ might
not give the expected result. In such scenario, it is recommended to create the Bifrost _create_usd_component_ compound manually (or to use your own python scripts to auto-generate it).
```

```
### Asset Versionning
If you add an empty **.versions** file in the component root directory, children directories will be considered 
as version directories. 
    
An additional *Asset Version* entry will apear in the Component Creator dialog.
```

```
Example:
```
	Shuttle <- Component root directory
	|_ .versions       <- empty file.
	|_ v001            <- version directory.
	| |_ geo
	|   |_ default.usd
	|_ v002            <- version directory.
	  |_ geo
	    |_ default.usd
	    
```
If you export your geometries using **Bifrost USD > File > Export Geometry**, an option will let you create a version. In this case, the **.versions** file will be automatically added to the component root directory.
