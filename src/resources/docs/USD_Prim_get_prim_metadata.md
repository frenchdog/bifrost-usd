# `get_prim_metadata`

Gets the value of a prim's metadata.

## Inputs

### `path`
The path to the USD prim. 

### `key`
The metadatum key. 

### `stage`
The USD stage. 

### `default_and_type`
The type of Bifrost value, and the default value if the metadatum could not be returned. This works similarly to the type on `get_geo_property` and similar nodes.

## Outputs

### `value`
The metadatum value. 

### `success`
Boolean indicating whether the operation was successful.

