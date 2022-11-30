from Particle import Particle

X_AXIS = True
Y_AXIS = False

X = 0
Y = 1


class BinarySearchTree:
    class Node:
        def __init__(self, pos: list, axis: bool, size):
            self.pos = pos
            self.axis = axis
            self.size = size

            self.left = None
            self.right = None

        def compare_to(self, pos: list):
            if self.axis == X_AXIS:
                return pos[X] - self.pos[X]
            else:
                return pos[Y] - self.pos[Y]

        def equals_to(self, pos: list):
            return self.pos[X] == pos[X] and self.pos[Y] == pos[Y]

        def dist_to(self, pos: list):
            return (self.pos[X] - pos[X]) ** 2 + (self.pos[Y] - pos[Y]) ** 2

    def __init__(self):
        self.root = None

    def __size__(self, node: Node):
        if node is None:
            return 0
        else:
            return node.size

    def __contains__(self, node: Node, pos: list, axis: bool):
        if node is None:
            return False
        if node.equals_to(pos):
            return True

        comp = node.compare_to(pos)
        if comp < 0:
            return self.__contains__(node.left, pos, not axis)
        else:
            return self.__contains__(node.right, pos, not axis)

    def contains(self, pos: list):
        if pos is None:
            raise Exception("Null argument to insert()")

        return self.__contains__(self.root, pos, X_AXIS)

    def __insert__(self, node: Node, pos: list, axis: bool):
        if node is None:
            return self.Node(pos, axis=axis, size=1)

        comp = node.compare_to(pos)

        if comp < 0:
            node.left = self.__insert__(node.left, pos, not axis)
        else:
            node.right = self.__insert__(node.right, pos, not axis)

        node.size = self.__size__(node.left) + self.__size__(node.right)

        return node

    def insert(self, pos: list):
        if pos is None:
            raise Exception("Null argument to insert()")

        self.root = self.__insert__(node=self.root, pos=pos, axis=X_AXIS)

    def nearest_neighbour(self, pos: list):
        nearest = self.__nearest_neighbour__(self.root, pos)

        return nearest.pos

    def nearest_neighbour_dist(self, pos: list):
        nearest = self.__nearest_neighbour__(self.root, pos)

        return nearest.dist_to(pos)

    def __closer_distance__(self, pivot, n1: Node, n2: Node):
        if n1 is None:
            return n2

        if n2 is None:
            return n1

        d1 = n1.dist_to(pivot)
        d2 = n2.dist_to(pivot)

        if d1 < d2:
            return n1
        else:
            return n2

    def __nearest_neighbour__(self, node: Node, pos: list):
        if node is None:
            return None

        comp = node.compare_to(pos)

        if comp < 0:
            first = node.left
            second = node.right

        else:
            first = node.right
            second = node.left

        nearest = self.__closer_distance__(pos, self.__nearest_neighbour__(first, pos), node)
        if nearest.dist_to(pos) >= comp:
            nearest = self.__closer_distance__(pos, self.__nearest_neighbour__(second, pos), nearest)

        return nearest


if __name__ == "__main__":
    bst = BinarySearchTree()

    bst.insert([1, 1])
    bst.insert([9, 9])
    # bst.insert([2, 2])

    print(bst.nearest_neighbour([2, 2]).pos)
