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


def apply(node, value):
    if not cmds.attributeQuery("BIF_material_hint", node=node, exists=True):
        cmds.addAttr(node, sn="mt", ln="BIF_material_hint", dt="string")
    cmds.setAttr(node + ".BIF_material_hint", value, type="string")

    if not cmds.attributeQuery(
        "USD_UserExportedAttributesJson", node=node, exists=True
    ):
        cmds.addAttr(
            node,
            ci=True,
            sn="USD_UserExportedAttributesJson",
            ln="USD_UserExportedAttributesJson",
            dt="string",
        )
    cmds.setAttr(
        f"{node}.USD_UserExportedAttributesJson",
        '{"BIF_material_hint": {"usdAttrName": "bifrost:material_hint", "usdAttrType": "primvar"}}',
        type="string",
    )


def apply_to_selection(value):
    for node in cmds.ls(selection=True, absoluteName=False):
        apply(node, value)


if __name__ == "__main__":
    apply_to_selection("metal")
