from .param_treenode import ParameterizedTreeNode
from ..vec import Vec3


class ParameterizedSpaceNode(ParameterizedTreeNode):

    # ------ transforms ------

    def to_local_position(self, outside_pos: Vec3):
        """
        Convert position to local coordinates.

        :param outside_pos: Vec3
        :return: Vec3
        """
        return outside_pos

    def from_local_position(self, local_pos: Vec3):
        """
        Convert local position to outside coordinates.

        :param local_pos: Vec3
        :return: Vec3
        """
        return local_pos

    def global_to_local_position(self, global_pos: Vec3):
        node = self
        nodes = []
        while node:
            nodes.append(node)
            node = node.node_parent

        pos = global_pos
        for node in reversed(nodes):
            pos = node.to_local_position(pos)

        return pos

    def local_to_global_position(self, local_pos: Vec3):
        node = self
        pos = local_pos
        while node is not None:
            pos = node.from_local_position(pos)
            node = node.node_parent

        return pos
