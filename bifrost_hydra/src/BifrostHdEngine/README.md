# Bifrost Hydra Engine - Executing Bifrost at Hydra Render time

The BifrostHdEngine library is responsible for:
1. Loading specific definitions (the JSON files describing nodes, compounds, types, etc.) into the Bifrost Library
2. Setting a graph (a graph can be a Bifrost compound or a Bifrost graph)
3. Setting the graph inputs using USD primvars matching their names
4. Executing the graph
5. Accessing the result, that is the output(s) of the graph

## Engine

The _BifrostHd::Engine_ is instantiated by the _Bifrost Hydra Generative Procedural_.
Its purpose is to simplify the setup of Bifrost at render time, hiding configuration steps, loading of the graph,
setting of the inputs, etc.

It is providing four methods:
1. _setInputScene(PXR_NS::HdSceneIndexBaseRefPtr inputScene)_
2. _setInputs(const PXR_NS::HdSceneIndexPrim& prim)_ // the Hydra Generative Procedural prim.
3. _execute(const double frame)_
4. _getOutput()_

## Executor's Workspace

The _BifrostHd::Workspace_ is responsible for loading the definition files. It is finding so called "JSON config files"
using the environment variable _BIFROST_LIB_CONFIG_FILES_ that can points to several JSON files at different locations.
For example, in our tests, we load the following JSON config file _${BIFROST_LOCATION}/resources/standalone_config.json_
for the usual Bifrost nodes and compounds, along with the JSON config file
_bifrost-usd/test/BifrostHydra/test_bif_geo_compounds_config.json_ that is loading extra compounds only used by the tests.

## Executor's GraphContainer

The Executor's _GraphContainer_ allows to load a graph, compile it then obtain a _Job_ from it:

1. _setGraph_ : Set the graph to execute into the _GraphContainer_
2. _compile_  : Compile the currently set graph
3. _getJob_   : Get the _Job_ responsible to execute the loaded graph

## Executor's Job

The Executor's _Job_ allows to set graph's inputs, execute it, then retrieve its outputs:

1. _getInputs_  : Get the job's inputs.
2. _execute_    : Execute the job with current inputs.
3. _getOutputs_ : Get the job's outputs.

## Parameters

The _BifrostHd::Parameters_ stores the _Pixar VtValues_ coming from the Hydra Generative Procedural of type _BifrostGraph_ that are:
1. The name of the Bifrost graph
2. The primvars used to the set the graph inputs
3. The Bifrost output of the graph you want to render in Hydra

## JobTranslationData

The _BifrostHd::JobTranslationData_ is an object that is used by the _BifrostHd::Engine_ to pass the parameters and time
to Bifrost while executing a graph.

## InputValueData

The _BifrostHd::InputValueData_ is used by the translation system to convert a Pixar _VtValue_ to an _Amino::Any_
(a Bifrost graph sets its inputs using Amino Any).

## OutputValueData

The _BifrostHd::OutputValueData_ is used by the translation system to convert an _Amino::Any_ to an Hydra prim.

## TypeTranslation

At graph execution, for each input value, Bifrost will call _convertValueFromHost_ on the _BifrostHd::TypeTranslation_
using a _BifrostHd::InputValueData_.
For each output value, Bifrost will call _convertValueToHost_ on the _BifrostHd::TypeTranslation_ to set the output
of the graph. Note that at the moment, the graph's output is a Bifrost Object and the translation to an Hydra prim
is done in the _Bifrost Hydra Generative Procedural_. Such design could change since it could convert the output value
to an Hydra Data Source Container instead.
