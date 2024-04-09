# `EditTarget`

This graph illustrates how to select a [sublayer](https://graphics.pixar.com/usd/release/glossary.html#usdglossary-sublayers) in a stage's root [layerStack](https://graphics.pixar.com/usd/release/glossary.html#usdglossary-rootlayerstack) as mentioned in the [EditTarget](https://graphics.pixar.com/usd/release/glossary.html#edittarget) section from the Open USD glossary.

It allows you to create or author prims, attributes and metadata in the targeted layer.

If you open the Maya USD Layer Editor on the stage created by this graph, by using the right click menu to print the layer content in the script editor you will see that:


- **my_model.usd** only store sublayers identifiers and the stage axis metadata
- **my_color.usd** only store the displayColor attribute applied to the modeling
- **my_modeling.usd** only store Capsule prim
