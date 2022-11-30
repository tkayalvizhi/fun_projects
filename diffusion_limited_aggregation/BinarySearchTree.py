from dla import Particle

X_AXIS = True
Y_AXIS = False


class BinarySearchTree:
    class Node:
        def __init__(self, particle: Particle, axis: bool, size):
            self.x, self.y = particle.get_xy()
            self.axis = axis
            self.size = size

            self.left = None
            self.right = None

        def compare_to(self, particle: Particle):
            if self.axis == X_AXIS:
                return self.x - particle.x
            else:
                return self.y - particle.y

        def equals_to(self, particle: Particle):
            return self.x == particle.x and self.y == particle.y

    def __init__(self):
        self.root = None

    def _contains_(self, node: Node, particle: Particle, axis: bool):
        if node is None:
            return False
        if node.equals_to(particle):
            return True

        comp = node.compare_to(particle)
        if comp < 0:
            return self._contains_(node.left, particle, not axis)
        else:
            return self._contains_(node.right, particle, not axis)

    def contains(self, particle: Particle):
        if particle is None:
            raise Exception("Null argument to insert()")

        return self._contains_(self.root, particle, X_AXIS)

    def _insert_(self, node: Node, particle: Particle, axis: bool):
        if node is None:
            return self.Node(particle, axis=axis, size=1)

        comp = node.compare_to(particle)

        if comp < 0:
            node.left = self._insert_(node.left, particle, not axis)
        else:
            node.right = self._insert_(node.right, particle, not axis)

        node.size = node.left.size + node.right.size

        return node

    def insert(self, particle: Particle):
        if particle is None:
            raise Exception("Null argument to insert()")

        self.root = self._insert_(node=self.root, particle=particle, axis=X_AXIS)