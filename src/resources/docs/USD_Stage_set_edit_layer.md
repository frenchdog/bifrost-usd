# `set_edit_layer`

This node sets the stage's EditTarget to the specified layer.

## Inputs

### `stage`
The stage in which to set the edit layer. 

### `layer_index`
The sublayer index to set as the stage's EditTarget. The last element in the list of sublayers is the strongest of the sublayers in the Pixar USD root layer. The index -1 identifies the root layer. If the index is not -1 and does not identify an existing sublayer, this node does nothing and the current stage's EditTarget is preserved. 


## Outputs
