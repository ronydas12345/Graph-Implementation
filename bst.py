class Node:
    def __init__(self, v, l=None, r=None, p=None):
        self.val = v
        self.left = l
        self.right = r
        self.parent = p

class BST:
    def __init__(self, r):
        self.root = r

    def get_height(self, node):
        if not node:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_bf(self, node):
        return self.get_height(node.right) - self.get_height(node.left)

    def update(self, ref):
        node = ref
        while node:
            bf = self.get_bf(node)
            if bf < -1:
                if self.get_bf(node.left) <= 0:
                    node = self.right_rotate(node)
                else:
                    node.left = self.left_rotate(node.left)
                    node = self.right_rotate(node)
            elif bf > 1:
                if self.get_bf(node.right) >= 0:
                    node = self.left_rotate(node)
                else:
                    node.right = self.right_rotate(node.right)
                    node = self.left_rotate(node)
            node = node.parent

    def append(self, val):
        cur = self.root
        while True:
            if val < cur.val:
                if not cur.left:
                    cur.left = Node(val, p=cur)
                    self.update(cur.left)
                    break
                cur = cur.left
            else:
                if not cur.right:
                    cur.right = Node(val, p=cur)
                    self.update(cur.right)
                    break
                cur = cur.right
    
    def delete_deepest(self, root, node):
        queue = [root]
        while queue:
            curr = queue.pop(0)
            if curr.left:
                if curr.left == node:
                    curr.left = None
                    return
                queue.append(curr.left)
            if curr.right:
                if curr.right == node:
                    curr.right = None
                    return
                queue.append(curr.right)
    
    def find(self, val):
        curr = self.root
        while curr:
            if val == curr.val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return None
    
    def replace(self, a, b):
        if not a.parent: self.root = b
        elif a == a.parent.left: a.parent.left = b
        else: a.parent.right = b
        if b: b.parent = a.parent

    def delete(self, val):
        node = self.find(val)
        if not node:
            return

        if not node.left: # no left child -> right child
            parent = node.parent
            self.replace(node, node.right)
            self.update(parent)
        elif not node.right: # no right child -> left child
            parent = node.parent
            self.replace(node, node.left)
            self.update(parent)
        else: # 2 children
            """
            find inorder successor
            swap values node to delete
            delete successor(at most 1 child)
            """
            next = node.right
            while next.left:
                next = next.left
            leftmost_parent = next.parent
            if next.parent != node:
                self.replace(next, next.right)
                next.right = node.right
                if next.right:
                    next.right.parent = next
            self.replace(node, next)
            next.left = node.left
            if next.left:
                next.left.parent = next
            self.update(leftmost_parent)#.parent)

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        return y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y
        return y

    def preorder(self, node):
        if not node: return
        print(node.val, end=' ')
        self.preorder(node.left)
        self.preorder(node.right)

    def inorder(self, node):
        if not node: return
        self.inorder(node.left)
        print(node.val, end=' ')
        self.inorder(node.right)

    def postorder(self, node):
        if not node: return
        self.postorder(node.left)
        self.postorder(node.right)
        print(node.val, end=' ')

bst = BST(Node(10))
for v in [20, 30, 5, 3, 4, 50, 60, 70]:
    bst.append(v)

print("Preorder:")
bst.preorder(bst.root)
print("\nInorder:")
bst.inorder(bst.root)
print("\nPostorder:")
bst.postorder(bst.root)
print()
"""
bst.delete(5)
print("\n\nDelete 5:")
print("Preorder:")
bst.preorder(bst.root)
print("\nInorder:")
bst.inorder(bst.root)
print("\nPostorder:")
bst.postorder(bst.root)
print()

bst.delete(10)
print("\n\nDelete 10:")
print("Preorder:")
bst.preorder(bst.root)
print("\nInorder:")
bst.inorder(bst.root)
print("\nPostorder:")
bst.postorder(bst.root)
print()
"""
bst.delete(4)
print("\n\nDelete 4:")
print("Preorder:")
bst.preorder(bst.root)
print("\nInorder:")
bst.inorder(bst.root)
print("\nPostorder:")
bst.postorder(bst.root)
print()