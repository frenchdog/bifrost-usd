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

#==============================================================================
# Relative structures

set(BIFROST_USD_PACK_INSTALL_RES_DIR             "${BIFUSD_INSTALL_COMMON_DIR}/resources")
set(BIFROST_USD_PACK_INSTALL_RES_JSON_DIR        "${BIFROST_USD_PACK_INSTALL_RES_DIR}/json")
set(BIFROST_USD_PACK_INSTALL_RES_ICONS_DIR       "${BIFROST_USD_PACK_INSTALL_RES_DIR}/icons")
set(BIFROST_USD_PACK_INSTALL_RES_DOCS_DIR        "${BIFROST_USD_PACK_INSTALL_RES_DIR}/docs")
set(BIFROST_USD_PACK_INSTALL_RES_CONFIG_DIR      "${BIFROST_USD_PACK_INSTALL_RES_DIR}/config")
set(BIFROST_USD_PACK_INSTALL_RES_PROC_DIR        "${BIFROST_USD_PACK_INSTALL_RES_DIR}/procedural")

# TODO: is "usd_pack" or the name of the config file defined somewhere?
set(BIFROST_USD_PACK_INSTALL_CONFIG_FILE         "usd_pack/usd_pack_config.json")

set(BIFROST_USD_PACK_SHARED_LIB_DIR ${BIFUSD_INSTALL_LIB_DIR})
if( BIFUSD_IS_WINDOWS)
    set(BIFROST_USD_PACK_SHARED_LIB_DIR ${BIFUSD_INSTALL_BIN_DIR})
endif()

file(RELATIVE_PATH BIFROST_USD_CONFIG_JSON        "/${BIFUSD_INSTALL_ROOT_DIR}" "/${BIFROST_USD_PACK_INSTALL_RES_JSON_DIR}")
file(RELATIVE_PATH BIFROST_USD_CONFIG_SHARED_LIB  "/${BIFUSD_INSTALL_ROOT_DIR}" "/${BIFROST_USD_PACK_SHARED_LIB_DIR}")

#==============================================================================
# Build resource outputs

set(BIFROST_USD_OUTPUT_JSON_DIR    "${PROJECT_BINARY_DIR}/${BIFROST_USD_PACK_INSTALL_RES_JSON_DIR}")
set(BIFROST_USD_OUTPUT_ICONS_DIR   "${PROJECT_BINARY_DIR}/${BIFROST_USD_PACK_INSTALL_RES_ICONS_DIR}")
set(BIFROST_USD_OUTPUT_DOCS_DIR    "${PROJECT_BINARY_DIR}/${BIFROST_USD_PACK_INSTALL_RES_DOCS_DIR}")
set(BIFROST_USD_OUTPUT_PROC_DIR    "${PROJECT_BINARY_DIR}/${BIFROST_USD_PACK_INSTALL_RES_PROC_DIR}")

set(BIFROST_USD_OUTPUT_LIB_CONFIG_FILE "${PROJECT_BINARY_DIR}/${BIFROST_USD_PACK_INSTALL_CONFIG_FILE}")

#==============================================================================
# External dependencies

bifusd_required_variables(USD_LOCATION)
list(APPEND CMAKE_MODULE_PATH "${BIFUSD_CMAKE_DIR}/modules")

if(IS_BIFUSD_STANDALONE)
    bifusd_required_variables(BIFROST_LOCATION)
    bifusd_required_variables(BIFUSD_PYTHON_EXECUTABLE)

    include(${BIFROST_LOCATION}/sdk/cmake/setup.cmake)

    if( BIFUSD_IS_WINDOWS)
        # Maya runtime location is optional.
        # If it is there we use it to find python dlls.
        # if not we use the python that we found to support
        # build steps.
        if(MAYA_RUNTIME_LOCATION)
            set(python_dir ${MAYA_RUNTIME_LOCATION}/bin)
        else()
            get_filename_component( python_dir ${BIFUSD_PYTHON_EXECUTABLE} DIRECTORY)
        endif()
    endif()

    if( BIFUSD_IS_WINDOWS)
        set(bifrost_lib_paths
            ${BIFROST_LOCATION}/bin
            ${BIFROST_LOCATION}/thirdparty/bin
            ${USD_LOCATION}/lib
            ${python_dir})

        # On Windows, the path to shared libraries must be explicitly
        # specified. While on Unix platforms, the libraries are automatically found
        # through the RPATH mechanism. Note that the default bifusd shared library
        # directory is always implicitly appended.
        set( BIFUSD_EXTRA_BUILD_AND_TEST_PATHS    "${bifrost_lib_paths}" )

    endif()
endif()

if( BIFUSD_IS_WINDOWS)
    # Add properties to be able to merge of json files and run tests externally
    set_target_properties( ${BIFUSD_PACKAGE_NAME}_config_info PROPERTIES
        BIFUSD_EXTRA_WIN_LIBS "${BIFUSD_EXTRA_BUILD_AND_TEST_PATHS}"
    )
endif()

# Add properties to be able to merge of json files and run tests externally
set_target_properties( ${BIFUSD_PACKAGE_NAME}_config_info PROPERTIES
    BIFROST_USD_PACK_ALL_JSON_FILES       ""
    BIFROST_USD_PACK_ALL_JSON_FILES_DIR   "${BIFROST_USD_OUTPUT_JSON_DIR}"
    BIFROST_USD_PACK_INSTALL_RES_JSON_DIR "${BIFROST_USD_PACK_INSTALL_RES_JSON_DIR}"
    BIFROST_USD_LIB_CONFIG_FILE           "${BIFROST_USD_OUTPUT_LIB_CONFIG_FILE}"
    BIFROST_USD_CONFIG_SHARED_LIB         "${BIFUSD_INSTALL_ROOT_DIR}/${BIFROST_USD_CONFIG_SHARED_LIB}"
)
