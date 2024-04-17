# `USD::Prim::define_usd_geom_subset`

Define a USD GeomSubset that is storing an array of face ids.

> <span style="color:#FFA07A">From bifrost-usd-lab pack. Included in namespace **USD::Prim**</span>

### `path`

The path of the prim definition of type GeomSubset.

### `element_type`

The type of elements this geometry subset includes. Only "face" is supported by USD at the moment.

### `indices`

The set of indices included in this subset. 
The indices need not be sorted, but the same index should not appear more than once.

### `family_name`

The name of the family of subsets that this subset belongs to. 
This is optional and can be used when roundtripping subset between DCC apps.
