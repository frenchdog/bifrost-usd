# -
# *****************************************************************************
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
# *****************************************************************************
# +
from maya import cmds
from bifrost_usd.component_creator.component import rename_default_model_variant


def show():
    rtn = cmds.promptDialog(
        title="USD Component",
        message="Rename Current Model Variant",
        button=["Ok", "Cancel"],
        defaultButton="Ok",
        cancelButton="Cancel",
        dismissString="Cancel",
    )

    if rtn == "Ok":
        rename_default_model_variant(cmds.promptDialog(query=True, text=True))


if __name__ == "__main__":
    show()