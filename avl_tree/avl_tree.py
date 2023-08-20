from avl_node import AVLNode

class AVLTree:
    """
        A lot of functions are also defined in AVLNode.
        Reason: seemed more OOP friendly for me
    """

    def __init__(self):
        """Default constructor. Initializes the AVL tree.
        """
        self.root = None

    def get_tree_root(self):
        """
        Method to get the root node of the AVLTree
        :return AVLNode -- the root node of the AVL tree
        """
        return self.root

    def get_tree_height(self):
        """Retrieves tree height.
        :return -1 in case of empty tree, current tree height otherwise.
        """
        if self.root is None:
            return -1

        return self.root.height

    def get_tree_size(self):
        """Yields number of key/value pairs in the tree.
        :return Number of key/value pairs.
        """
        if self.root is None:
            return 0

        counter = {"counter": 0}
        def count_pairs(node):
            counter["counter"] += 1

        self.root.preorder(count_pairs)
        return counter["counter"]

    def to_array(self):
        """Yields an array representation of the tree's values (pre-order).
        :return Array representation of the tree values.
        """
        q = []
        if self.root is None:
            return q
        
        self.root.preorder(lambda node : q.append(node.value))
        return q

    def find_by_key(self, key):
        """Returns value of node with given key.
        :param key: Key to search.
        :return Corresponding value if key was found, None otherwise.
        :raises ValueError if the key is None
        """
        if key is None:
            raise ValueError("Passed None key")
        
        if self.root is None:
            return None
        
        return self.root.find(key)

    def insert(self, key, value):
        """Inserts a new node into AVL tree.
        :param key: Key of the new node.
        :param value: Data of the new node. Must not be None. Nodes with the same key
        are not allowed. In this case False is returned. None-Keys and None-Values are
        not allowed. In this case an error is raised.
        :return True if the insert was successful, False otherwise.
        :raises ValueError if the key or value is None.
        """
        if key is None:
            raise ValueError("No key passed")

        if self.root is None:
            self.root = AVLNode(key, value)
            return True
        
        new_node = self.root.add_node(key, value)
        if new_node is not None:
            new_node.update_height()
            if new_node.parent is not None:
                new_node.parent.check_balanced(new_node, None)
            return True

        return False

    def remove_by_key(self, key):
        """Removes node with given key.
        :param key: Key of node to remove.
        :return True If node was found and deleted, False otherwise.
        @raises ValueError if the key is None.
        """
        if key is None:
            raise ValueError("No key passed")
        
        ctx = {"success": False}

        if self.root is None:
            return False

        self.remove(self.root, key, ctx)
        return ctx["success"]

    def _traverse_tree(self, node, fn):
        if node is None:
            return
        if node.left is not None:
            fn("L", node.left)
            self._traverse_tree(node.left, fn)
        if node.right is not None:
            fn("R", node.right)
            return self._traverse_tree(node.right, fn)
        
        fn("X", node)

    def remove(self, node, key, ctx):
        if node is None:
            return node
        
        if key < node.key:
            node.left = self.remove(node.left, key, ctx)
            if node.left is not None:
                    node.left.update_height()
                    node.left.check_balanced_removed()
        elif key > node.key:
            node.right = self.remove(node.right, key, ctx)
            if node.right is not None:
                    node.right.update_height()
                    node.right.check_balanced_removed()
        else:
            ctx["success"] = True
            if node.left is None:
                if node.right is not None:
                    node.right.parent = node.parent
                return node.right
            elif node.right is None:
                if node.left is not None:
                    node.left.parent = node.parent
                return node.left
            
            replacement = node.get_replacement()
            parent = replacement.parent
            node.key = replacement.key
            node.value = replacement.value
            node.right = self.remove(node.right, replacement.key, ctx)
            parent.update_height()
            parent.check_balanced_removed()

        return node

    



