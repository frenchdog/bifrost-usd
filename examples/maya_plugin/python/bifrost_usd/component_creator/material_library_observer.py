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

from bifrost_usd.component_creator.component import find_bifrost_component_graph
from bifrost_usd.component_creator.component import get_binding_nodes
from bifrost_usd.component_creator.component import hasComponentCreatorGraph
from bifrost_usd.component_creator.constants import kMatLibShapeFullName


from bifrost_usd.graph_api import GraphAPI


graphAPI = GraphAPI(find_bifrost_component_graph)

OBSERVER = None


def observed_path(changedPath):
    if str(changedPath.popSegment()) == "|world" + kMatLibShapeFullName:
        return True

    return False


class MaterialLibraryObserver(ufe.Observer):
    def __init__(self):
        super(MaterialLibraryObserver, self).__init__()

    def __call__(self, notification):
        if not observed_path(changedPath := notification.changedPath()):
            return

        if hasComponentCreatorGraph() is False:
            return

        if isinstance(notification, ufe.ObjectDelete):
            for node in get_binding_nodes():
                if graphAPI.param(node, "material") == str(changedPath.back()):
                    graphAPI.remove_node(node)

        if isinstance(notification, ufe.ObjectRename):
            for node in get_binding_nodes():
                if graphAPI.param(node, "material") == str(changedPath.back()):
                    newPath = notification.item().path()
                    graphAPI.set_param(node, ("material", str(newPath.back())))


def register():
    global OBSERVER
    OBSERVER = MaterialLibraryObserver()
    ufe.Scene.addObserver(OBSERVER)


def unregister():
    global OBSERVER
    if OBSERVER:
        ufe.Scene.removeObserver(OBSERVER)


if __name__ == "__main__":
    register()
