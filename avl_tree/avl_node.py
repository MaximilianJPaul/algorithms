class AVLNode:
    def __init__(self, key=0, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def to_string(self):
        return "key:" + str(self.key) + ", value: " + str(self.value)

    def add_node(self, key, value):
        if (key == self.key):
            return None
        elif key < self.key:
            if self.left is None:
                self.left = AVLNode(key, value)
                self.left.parent = self
                return self.left
            else:
                return self.left.add_node(key, value)
        elif key > self.key:
            if self.right is None:
                self.right = AVLNode(key, value)
                self.right.parent = self
                return self.right
            else:
                return self.right.add_node(key, value)

    def update_height(self):
        self.height = max(
            self.get_right_height(),
            self.get_left_height()) + 1
        if self.parent is not None:
            self.parent.update_height()

    def check_balanced(self, x, y = None):
        diff = abs(self.get_left_height() - self.get_right_height())
        if diff > 1:
            if y is not None:
                self.rebalance(x, y)
        if self.parent is not None:
            self.parent.check_balanced(y if y is not None else x, self)
        
    def check_balanced_removed(self):
        left, right = self.get_left_height(), self.get_right_height()
        diff = abs(left - right)
        highest_child = self.get_highest_child()
        if diff > 1 and highest_child is not None:
            self.rebalance(
                highest_child.get_highest_child(),
                highest_child
            )
        if self.parent is not None:
            self.parent.check_balanced_removed()

    def get_highest_child(self):
        return self.left if self.get_left_height() > self.get_right_height() else self.right

    def clone(self):
        return AVLNode(self.key, self.value)

    def rebalance(self, x, y):
        links = self.build_link_list(x, y)
        self.restructure(links)
        
        if self.left is not None:
            self.left.update_height()
        if self.right is not None:
            self.right.update_height()

    def build_link_list(self, x, y):
        if self.right == y and y.right == x:
            return [self.left, self.clone(), y.left, y, x.left, x, x.right]
        elif self.left == y and y.left == x:
            return [x.left, x.clone(), x.right, y, y.right, self.clone(), self.right]
        elif self.right == y and y.left == x:
            return [self.left, self.clone(), x.left, x, x.right, y, y.right]
        elif self.left == y and y.right == x:
            return [y.left, y, x.left, x, x.right, self.clone(), self.right]

    def restructure(self, list):
        [t0, a, t1, b, t2, c, t3] = list
        a.left = t0
        if t0 is not None:
            t0.parent = a
        a.right = t1
        if t1 is not None:
            t1.parent = a
            
        c.left = t2
        c.right = t3
        if t2 is not None:
            t2.parent = c
        if t3 is not None:
            t3.parent = c

        self.left = a
        self.right = c
        self.key = b.key
        self.value = b.value

        a.parent = self
        c.parent = self

    def get_left_height(self):
        return self.left.height if self.left is not None else -1
    
    def get_right_height(self):
        return self.right.height if self.right is not None else -1

    def get_replacement(self):
        curr = self.right

        while curr.left is not None:
            curr = curr.left
        
        return curr

    def find(self, key):
        if self.key == key:
            return self.value
        elif key < self.key and self.left is not None:
            return self.left.find(key)
        elif key > self.key and self.right is not None:
            return self.right.find(key)
        
        return None

    def preorder(self, fn):
        fn(self)
        if self.left is not None:
            self.left.preorder(fn)
        if self.right is not None:
            self.right.preorder(fn)