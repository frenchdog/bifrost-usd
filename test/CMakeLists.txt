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

set(resources_dir "${BIFUSD_TEST_RESOURCES_LOCATION}/resources")
set(usd_test_dir "${CMAKE_CURRENT_LIST_DIR}")

message( STATUS "BifrostUSD test dir.:           ${usd_test_dir}")
message( STATUS "BifrostUSD test resources dir.: ${resources_dir}")

if(NOT DEFINED BIFUSD_BIFCMD_LOCATION)
    bifusd_required_variables(BIFROST_LOCATION)
    set(BIFUSD_BIFCMD_LOCATION "${BIFROST_LOCATION}/bin")
endif()

# The google tests are causing some issues with Clang address sanitizer when linking with USD libraries.
# The sanitizer will detect some container overflows in USD libs just be creating
# an executable with the following empty google test "TEST(TEST_EMPTY, empty_test) {}"!
#
# See this ticket related to sanitizer errors in OpenUSD:
# https://github.com/PixarAnimationStudios/OpenUSD/issues/3088
if (NOT BIFUSD_ENABLE_ADDRESS_SANITIZER)
    set(asan_options ASAN_OPTIONS=detect_container_overflow=0)
endif()

add_subdirectory(BifrostUsd)
add_subdirectory(nodedefs)
