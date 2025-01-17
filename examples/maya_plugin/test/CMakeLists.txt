#-
#*****************************************************************************
# Copyright 2024 Autodesk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#*****************************************************************************
#+

set(python_tests
    testAssetTemplate.py
    testBifrostStageCmds.py
    testComponentCreator.py
    testComponentCreatorGraphOnly.py
    testComponentMaterialBinding.py
    testCreateComponentGraph.py
    testGetComponentMetadata.py
    testImportMayaModel.py
    testImportMayaModelInNewStage.py
    testImportMayaVariants.py
    testMaterialHintAttribute.py
    testModelExporter.py
    testPrimPath.py
    testValidateGeo.py
)

set(env_vars)

if(IS_BIFUSD_STANDALONE)
    # When running tests in standalone mode with BIFROST_LOCATION being defined,
    # we need to disable the default usd_pack that is shipped with bifrost.
    list(APPEND env_vars BIFROST_DISABLE_PACKS=usd_pack)
    list(APPEND env_vars "BIFROST_LIB_CONFIG_FILES=${CMAKE_INSTALL_PREFIX}/plugin_config.json:${BIFROST_LIB_CONFIG_FILES}")
endif()

set(USD_PYTHON_PATH "${MAYA_USD_PLUGIN_DIR}/mayausd/USD/lib/python")
set(MAYA_USD_PYTHON_PATH "${MAYA_USD_PLUGIN_DIR}/mayausd/MayaUSD/lib/python")

list(APPEND env_vars "PYTHONPATH=${USD_PYTHON_PATH}::${MAYA_USD_PYTHON_PATH}:${CMAKE_INSTALL_PREFIX}/${BIFUSD_INSTALL_ROOT_DIR}/examples/maya_plugin/python")
list(APPEND env_vars "MAYA_MODULE_PATH=${CMAKE_INSTALL_PREFIX}/${BIFUSD_INSTALL_ROOT_DIR}/examples/maya_plugin:${MAYA_USD_PLUGIN_DIR}:${LOOKDEVX_PLUGIN_DIR}:${BIFROST_LOCATION}/../../modules/")

foreach(test_file ${python_tests})
    add_test(NAME examples_${test_file}
             COMMAND "${MAYA_PY_EXECUTABLE}" ${CMAKE_CURRENT_SOURCE_DIR}/${test_file}
    )
    set_tests_properties(examples_${test_file} PROPERTIES ENVIRONMENT "${env_vars}")
    bifusd_set_test_shared_library_path(examples_${test_file} ${BIFUSD_EXTRA_BUILD_AND_TEST_PATHS})
endforeach()
