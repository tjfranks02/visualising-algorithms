"""
binary search tree implementation. contains all basic functionality
required to operate the tree.
"""

class Node:
    """
    class representing a node in a binary tree structure.
    nodes have a value plus a left and right child, which can
    be None or another node
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    def one_child(self):
        """
        determines whether node has exactly one child.

        returns (Node):
            the one child if found. None if the node doesn't 
            have exactly one child.
        """        
        if self.left != None and self.right == None:
            return self.left
        elif self.left == None and self.right != None:
            return self.right
        
        return None

    def no_children(self):
        """
        determines whether node has no children

        returns (bool):
            true if no children for this node. false
            otherwise.
        """      
        return self.left == None and self.right == None

    def both_children(self):
        """
        determines whether node has both children

        returns (Node):
            the one child if both children present. false
            otherwise
        """      
        return self.left != None and self.right != None

    """
    getters and setters
    """
    def set_value(self, value):
        self.value = value

    def set_left_child(self, left):
        self.left = left
    
    def set_right_child(self, right):
        self.right = right

    def get_value(self):
        return self.value

    def get_left_child(self):
        return self.left

    def get_right_child(self):
        return self.right


def create(value):
    """
    function to initialise an empty binary search tree.

    returns (Node):
        an empty binary search tree.
    """
    return Node(value)


def insert(root, value):
    """
    function to insert a node into a binary search tree.

    returns (Node):
        the binary search tree with the new node inserted.
        if a duplicate is encountered, the tree will be returned
        in an identical state.
    """
    if root == None:
        return Node(value)

    #make no changes if duplicate found
    if root.get_value() == value:
        return root

    if root.get_value() < value:
        root.right = insert(root.right, value)
    elif root.get_value() > value:
        root.left = insert(root.left, value)

    return root


def search(root, value):
    """
    function to search the binary search tree for a specified value

    parameters:
        root (Node): the tree to search
        value (int): the value to try and locate in the tree

    returns (Node):
        the node located with that value if found. none if there was no
        matching node in the binary search tree.
    """
    #value can't be found in the tree
    if root == None:
        return None

    #determine which node to search next
    if root.get_value() == value:
        return root
    elif root.get_value() < value:
        return search(root.get_right_child(), value)
    else:
        return search(root.get_left_child(), value)


def min_node(root):
    """
    given a node from a binary search tree, returns the node with the
    lowest value in the tree

    parameters:
        root (Node): the tree to search

    returns (Node):
        the node with the lowest value in the tree
    """
    if root.left == None:
        return root

    return min_node(root.left)


def delete(root, value):
    """
    attempts to delete the node with a specified value in the tree

    parameters:
        root (Node): the tree to delete from
        value (int): the value of the node to search for and delete

    returns (Node):
        the tree in an updated state after the deletion of the node.
        tree will be returned in an identical state if the value
        requested for deletion does not exist.
    """
    if root == None:
        return None

    if root.get_value() < value:
        root.right = delete(root.get_right_child(), value)
    elif root.get_value() > value:
        root.left = delete(root.get_left_child(), value)
    else:
        #this is the one to delete
        if root.no_children():
            root = None
        elif root.one_child():
            child = root.one_child()
            root = child
        else:
            minimum_node = min_node(root.right)
            root.set_value(minimum_node.get_value())
            delete(root.right, minimum_node.get_value())
    return root


def inorder(root):
    """
    perform an inorder traversal of the given binary search tree.

    parameters:
        root (Node): the tree on which the traversal will be performed

    returns (list[int]):
        list of node values visited during the traversal
    """
    if root == None:
        return []

    left_list = inorder(root.left)
    middle_value = [root.value]
    right_list = inorder(root.right)

    return left_list + middle_value + right_list


def preorder(root):
    """
    perform a preorder traversal on a given binary search tree.

    parameters:
        root (Node): the tree on which the traversal will be performed

    returns (list[int]):
        list of node values visited during the preorder traversal
    """
    if root == None:
        return []

    middle_value = [root.value]
    left_list = preorder(root.left)
    right_list = preorder(root.right)

    return middle_value + left_list + right_list


def postorder(root):    
    """
    perform a postorder traversal on a given binary search tree.

    parameters:
        root (Node): the tree on which the traversal will be performed

    returns (list[int]):
        list of node values visited during the postorder traversal
    """
    if root == None:
        return []

    left_list = postorder(root.left)
    right_list = postorder(root.right)
    middle_value = [root.value]

    return left_list + right_list + middle_value


def get_height(root):
    """
    function to get the height of a binary search tree.

    parameters:
        root (Node): the binary search tree to get the height of

    returns (int):
        the height of the binary tree (leaf node height = 1).
    """
    if root == None:
        return 0

    return max(1 + get_height(root.left), 1 + get_height(root.right))


def level_values(root, level):
    """
    function to get the value of every node at the requested level.

    parameters:
        root (Node): the binary search tree to get the values for
        level (int): the level to get the values for in the tree

    returns (list[int]):
        the list of values at the requested level in the search tree
    """
    if root == None:
        return []
    elif level == 1:
        return [root.get_value()]

    return level_values(root.left, level - 1) + \
        level_values(root.right, level - 1)


def breadth_first(root):
    """
    performs a breadth-first traversal of a given binary tree

    parameters:
        root (Node): the binary tree to perform the traversal on

    returns (list[int]):
        the list of node values visited during the traversal
    """
    height = get_height(root)
    node_values = []
    level = 1

    while level <= height:
        node_values += level_values(root, level)
        level += 1

    return node_values
    

root = create(50)
root = insert(root, 30)
root = insert(root, 20)
root = insert(root, 40)

root = insert(root, 70)
root = insert(root, 60)
root = insert(root, 80)

print(root.right.value)

#traversals
print(inorder(root))
print(preorder(root))
print(postorder(root))

print(get_height(root))

print(breadth_first(root))