from DLA_OLD import *
from DLA_OLD.Particle import Position


class BinarySearchTree:
    class Node:
        def __init__(self, pos: Position, axis: bool, size):
            self.pos = pos
            self.axis = axis
            self.size = size

            self.left = None
            self.right = None

        def compare_to(self, pos: Position):
            if self.axis == X_AXIS:
                return self.pos.x - pos.x
            else:
                return self.pos.y - pos.y

        def equals_to(self, pos: Position):
            return self.pos.x == pos.x and self.pos.y == pos.y

    def __init__(self):
        self.root = None

    def __size__(self, node: Node):
        if node is None:
            return 0
        else:
            return node.size

    def __contains__(self, node: Node, pos: Position, axis: bool):
        if node is None:
            return False
        if node.equals_to(pos):
            return True

        comp = node.compare_to(pos)
        if comp < 0:
            return self.__contains__(node.left, pos, not axis)
        else:
            return self.__contains__(node.right, pos, not axis)

    def contains(self, pos: Position):
        if pos is None:
            raise Exception("Null argument to insert()")

        return self.__contains__(self.root, pos, X_AXIS)

    def __insert__(self, node: Node, pos: Position, axis: bool):
        if node is None:
            return self.Node(pos, axis=axis, size=1)

        comp = node.compare_to(pos)

        if comp < 0:
            node.left = self.__insert__(node.left, pos, not axis)
        else:
            node.right = self.__insert__(node.right, pos, not axis)

        node.size = self.__size__(node.left) + self.__size__(node.right)

        return node

    def insert(self, pos: Position):
        if pos is None:
            raise Exception("Null argument to insert()")

        self.root = self.__insert__(node=self.root, pos=pos, axis=X_AXIS)
