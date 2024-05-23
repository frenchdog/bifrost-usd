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
import ufe

from bifrost_usd.author_usd_graph import delete_node
from bifrost_usd.author_usd_graph import has_bifrost_usd_graph
from bifrost_usd.author_usd_graph import is_supported_prim_type
from bifrost_usd.author_usd_graph import rename_nodes_path_parameter
from bifrost_usd.author_usd_graph import reparent_nodes_path_parameter
from bifrost_usd.author_usd_graph import to_prim_path
from bifrost_usd.author_usd_graph import graphAPI

from bifrost_usd.constants import kDefinePrimHierarchy


OBSERVER = None


def log(args):
    if graphAPI.ufe_observer:
        print(args)


class DagPathObserver(ufe.Observer):
    """Update a prim path when a DAG path is changed.
    If there is no Bifrost USD graph in the scene, do nothing."""

    def __init__(self):
        super(DagPathObserver, self).__init__()

    def __call__(self, notification):
        if not has_bifrost_usd_graph():
            return

        ufeChangedPath = notification.changedPath()

        if isinstance(notification, ufe.ObjectReparent):
            log(f"ObjectReparent: {ufeChangedPath}, {notification.item().path()}")
            newPrimPath = str(notification.item().path())
            if is_supported_prim_type(newPrimPath):
                reparent_nodes_path_parameter(
                    to_prim_path(str(ufeChangedPath)), to_prim_path(newPrimPath)
                )

        if isinstance(notification, ufe.ObjectPathRemove):
            log(f"ObjectPathRemove: {ufeChangedPath}, {notification.item().path()}")

        if isinstance(notification, ufe.ObjectRename):
            log(f"ObjectRename: {ufeChangedPath}, {notification.item().path()}")
            newPath = str(notification.item().path())
            if is_supported_prim_type(newPath):
                rename_nodes_path_parameter(
                    to_prim_path(str(ufeChangedPath)), to_prim_path(newPath)
                )

        if isinstance(notification, ufe.ObjectPathAdd):
            log(f"ObjectPathAdd: {ufeChangedPath}, {notification.item().path()}")

        if isinstance(notification, ufe.ObjectAdd):
            log(f"ObjectAdd: {ufeChangedPath}, {notification.item().path()}")

        if isinstance(notification, ufe.ObjectDelete):
            log(f"ObjectDelete: {ufeChangedPath}")
            if primPath := to_prim_path(str(ufeChangedPath)):
                delete_node(
                    primPath,
                    node_type=kDefinePrimHierarchy,
                )


def register():
    global OBSERVER
    OBSERVER = DagPathObserver()
    ufe.Scene.addObserver(OBSERVER)


def unregister():
    global OBSERVER
    if OBSERVER:
        ufe.Scene.removeObserver(OBSERVER)
