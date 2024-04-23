# CS 302 Program 4/5 tree.py
# Alan Shirk 3/19/24
# A Red-Black Tree to use for the player's inventory. The player can retrieve and use items based on their keys

# Nodes for the red black tree
class Node:
    def __init__(self, item, color='red'):
        self.item = item
        self.left = None
        self.right = None
        self.color = color

# Red-black tree for hero inventory
class Red_Black_Tree:
    def __init__(self):
        self._root = None
        self._duplicates = []

    # insert functions
    def insert(self, item):
        self._root = self._insert_recursive(self._root, item)
        self._root.color = 'black'  # set root to black

    def _insert_recursive(self, node, item):
        if node is None:
            return Node(item)

        if item._key < node.item._key:
            node.left = self._insert_recursive(node.left, item)
        elif item._key > node.item._key:
            node.right = self._insert_recursive(node.right, item)
        else:  # duplicate, append to list and throw error
            self._duplicates.append(item)
            raise ValueError("Error, attempted to insert with duplicate key")

        # rotate and flip colors if necessary
        if self._is_red(node.right) and not self._is_red(node.left):
            node = self._rotate_left(node)
        if self._is_red(node.left) and self._is_red(node.left.left):
            node = self._rotate_right(node)
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(node)

        return node

    # retrieval
    def retrieve(self, key):
        return self._retrieve_recursive(self._root, key)

    def _retrieve_recursive(self, node, key):
        if node is None:
            return None

        if key < node.item._key:
            return self._retrieve_recursive(node.left, key)
        elif key > node.item._key:
            return self._retrieve_recursive(node.right, key)
        else:
            return node.item

    # display
    def display(self):
        self._display_recursive(self._root)

    def _display_recursive(self, node, level=0):
        if node:
            self._display_recursive(node.right, level + 1)
            print(' ' * 4 * level + '-', node.item._name)
            self._display_recursive(node.left, level + 1)

    # show inventory to user
    def show_items(self):
        print("=== Inventory ===")
        self._show_items_recursive(self._root)
        print()

    def _show_items_recursive(self, node):
        if node:
            self._show_items_recursive(node.left)
            print(f"({node.item._key}) - {node.item._name}")
            self._show_items_recursive(node.right)

    # red-black tree helper functions 
    def _is_red(self, node):
        if node is None:
            return False
        return node.color == 'red'

    def _rotate_left(self, node):
        right_node = node.right
        node.right = right_node.left
        right_node.left = node
        right_node.color = node.color
        node.color = 'red'
        return right_node

    def _rotate_right(self, node):
        left_node = node.left
        node.left = left_node.right
        left_node.right = node
        left_node.color = node.color
        node.color = 'red'
        return left_node

    def _flip_colors(self, node):
        node.color = 'red'
        node.left.color = 'black'
        node.right.color = 'black'

    # removal
    def delete(self, key):
        self._root = self._delete_recursive(self._root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return node

        # in left subtree
        if key < node.item._key:
            node.left = self._delete_recursive(node.left, key)

        # in right subtree
        elif key > node.item._key:
            node.right = self._delete_recursive(node.right, key)

        # equal keys
        else:
            # node with only one child or no child
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            # node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._min_value_node(node.right)

            # copy the inorder successor's content to this node
            node.item = temp.item

            # delete the inorder successor
            node.right = self._delete_recursive(node.right, temp.item._key)

        return node

    def _min_value_node(self, node):
        current = node

        # loop down to find the leftmost leaf
        while current.left is not None:
            current = current.left

        return current