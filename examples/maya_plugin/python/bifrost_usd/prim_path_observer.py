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


class PrimPathObserver(ufe.Observer):
    def __init__(self):
        super(PrimPathObserver, self).__init__()

    def __call__(self, notification):
        if not has_bifrost_usd_graph():
            return

        changedPath = notification.changedPath()

        if isinstance(notification, ufe.ObjectReparent):
            log(
                f"ObjectReparent: {notification.changedPath()}, {notification.item().path()}"
            )
            newPrimPath = str(notification.item().path())
            if is_supported_prim_type(newPrimPath):
                reparent_nodes_path_parameter(
                    to_prim_path(str(changedPath)), to_prim_path(newPrimPath))

        if isinstance(notification, ufe.ObjectPathRemove):
            log(
                f"ObjectPathRemove: {notification.changedPath()}, {notification.item().path()}"
            )

        if isinstance(notification, ufe.ObjectRename):
            log(
                f"ObjectRename: {notification.changedPath()}, {notification.item().path()}"
            )
            newPath = str(notification.item().path())
            if is_supported_prim_type(newPath):
                rename_nodes_path_parameter(
                    to_prim_path(str(changedPath)), to_prim_path(newPath)
                )

        if isinstance(notification, ufe.ObjectPathAdd):
            log(
                f"ObjectPathAdd: {notification.changedPath()}, {notification.item().path()}"
            )

        if isinstance(notification, ufe.ObjectAdd):
            log(
                f"ObjectAdd: {notification.changedPath()}, {notification.item().path()}"
            )

        if isinstance(notification, ufe.ObjectDelete):
            log(f"ObjectDelete: {notification.changedPath()}")
            if primPath := to_prim_path(str(changedPath)):
                delete_node(
                    primPath,
                    node_type=kDefinePrimHierarchy,
                )


def register():
    global OBSERVER
    OBSERVER = PrimPathObserver()
    ufe.Scene.addObserver(OBSERVER)


def unregister():
    global OBSERVER
    if OBSERVER:
        ufe.Scene.removeObserver(OBSERVER)
