# -
# *****************************************************************************
# Copyright 2024 Autodesk, Inc.
#
# Licensed under the Apache License, Version 2.0(the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License                    at
#
# http: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on   an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# *****************************************************************************
# +
from typing import Any
from dataclasses import dataclass
from maya import cmds


@dataclass
class MayaUSDAttribute:
    name: str
    value: Any
    typeName: str


def get_mayausd_attributes(dag_path: str) -> list[Any]:
    attrNames = cmds.listAttr(dag_path, userDefined=True)
    if attrNames is None:
        return []

    result: list[Any] = []
    for name in attrNames:
        if name.startswith("USD_"):
            value = cmds.getAttr(f"{dag_path}.{name}")
            typeName = cmds.getAttr(f"{dag_path}.{name}", type=True)
            if typeName:
                if typeName == "string":
                    if value is None:
                        value = ""
                assert (
                    typeName == "string" or typeName == "bool"
                ), f"Maya USD attribute should be a string or a bool on {dag_path}"
                result.append(MayaUSDAttribute(name, value, typeName))

    return result


def get_prim_type_from_maya_usd_attrib(dag_path: str, defaultType="Xform") -> str:
    primType = defaultType
    for attrib in get_mayausd_attributes(dag_path):
        if attrib.name == "USD_typeName":
            primType = attrib.value
            break

    return primType


def get_parent_dag_path(dag_path: str) -> str:
    parent = cmds.listRelatives(dag_path, parent=True, fullPath=True)
    if parent is None:
        return ""
    return parent[0]


def get_all_prim_types(dag_path: str, defaultType="Xform") -> list[str]:
    """Gives all the USD prim types from a Maya hierarchy.
    The prim type is found from the 'USD_typeName' attribute on every DAG nodes of the hierarchy.
    If this attribute is not found, it uses the defaultType.

    :return: The USD type names in same order than the DAG hierarchy.
    """
    prim_types: list[str] = []

    dagPath = dag_path
    while dagPath:
        prim_types.append(get_prim_type_from_maya_usd_attrib(dagPath))
        dagPath = get_parent_dag_path(dagPath)

    return prim_types
