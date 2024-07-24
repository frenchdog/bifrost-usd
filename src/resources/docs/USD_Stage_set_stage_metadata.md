# `set_stage_metadata`

This node sets the value of a stage metadatum if the stage's current UsdEditTarget is the root or session layer.

## Inputs

### `key`
The metadatum key. 

### `value`
The metadatum value. 

### `stage`
The stage in which to set the metadatum. 

## Outputs

### `out_stage`
The modified USD stage. 

### `success`
Boolean indicating whether the operation was successful.
