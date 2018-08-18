import random
import copy


class TreapNode:
    def __init__(self, key, rand):
        self.key = key
        # since random() gives value between 0 and 1, we need our split x to be > 1
        self.priority = random.random() if rand else 1.1
        self.left = None
        self.right = None

    def rotate_right(self):
        y = self
        x = y.left

        y.left = x.right
        x.right = y
        y = x

        return y

    def rotate_left(self):
        y = self
        x = y.right

        y.right = x.left
        x.left = y
        y = x

        return y

    def print(self, node):
        if node is None:
            return
        print('key: ', node.key)
        if node.left is not None:
            print(' left: ', node.left.key)
        if node.right is not None:
            print(' right: ', node.right.key)
        self.print(node.left)
        self.print(node.right)


class Treap:
    def __init__(self):
        self.root = None

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if node.key < key:
            return self._search(node.right, key)

        return self._search(node.left, key)

    def search(self, key):
        return self._search(self.root, key)

    def _insert(self, node, key, rand):
        if node is None:
            node = TreapNode(key, rand)
            return node
        if node.key >= key:
            node.left = self._insert(node.left, key, rand)
            if node.left.priority > node.priority:
                node = node.rotate_right()
        else:
            node.right = self._insert(node.right, key, rand)
            if node.right.priority > node.priority:
                node = node.rotate_left()

        return node

    def insert(self, key):
        self.root = self._insert(self.root, key, True)

    def _delete(self, node, key):
        if node is None:
            return False
        if node.key == key:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.priority < node.right.priority:
                    node = node.rotate_right()
                    node.right = self._delete(node.right, key)
                else:
                    node = node.rotate_left()
                    node.left = self._delete(node.left, key)
        elif node.key > key:
            node.left = self._delete(node.left, key)
        else:
            node.right = self._delete(node.right, key)
        return node

    def delete(self, key):
        if self.search(key) is None:
            return False
        self.root = self._delete(self.root, key)
        return True

    def split(self, key):
        self.root = self._insert(self.root, key, False)
        t1, t2 = copy.deepcopy(self.root.left), copy.deepcopy(self.root.right)
        self.delete(key)
        return t1, t2

    def _pre_order(self, node):
        if node is None:
            return
        print('key: ', node.key, ' priority: ', node.priority)
        if node.left is not None:
            print(' left: ', node.left.key)
        if node.right is not None:
            print(' right: ', node.right.key)
        self._pre_order(node.left)
        self._pre_order(node.right)

    def pre_order(self):
        self._pre_order(self.root)


root = Treap()

root.insert(10)
root.insert(20)
root.insert(5)
root.insert(40)
root.insert(100)
root.insert(1)
root.insert(50)
root.insert(30)
l, r = root.split(35)

print('left part:\n')
l.print(l)
print('\nright part:\n')
r.print(r)
print('\ntreap')
root.pre_order()
