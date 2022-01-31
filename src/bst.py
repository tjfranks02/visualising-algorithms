"""
binary search tree implementation. contains all basic functionality
required to operate the tree.
"""

import copy
import sys

"""
instructions describing all binary search tree operations. used to describe the
path taken to perform insert, delete, search actions.
"""
FIND = "FIND"
SEARCH = "SEARCH"
SWAP = "SWAP"
INSERT = "INSERT"
NOT_FOUND = "NOT_FOUND"
DUPLICATE = "DUPLICATE"
DELETE = "DELETE"
RESTRUCTURE = "RESTRUCTURE"


class Node:
    """
    class representing a node in a binary tree structure.
    nodes have a value plus a left and right child, which can
    be None or another node
    """
    def __init__(self, value, left=None, right=None):
        """
        parameters:
            value (int): the value that this tree node stores.
        """
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
        determines whether node has no children.

        returns (bool):
            true if no children for this node. false
            otherwise.
        """      
        return self.left == None and self.right == None

    def both_children(self):
        """
        determines whether node has both children.

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


def h_delete(root, value, path):
    """
    attempts to delete the node with a specified value in the tree

    parameters:
        root (Node): the tree to delete from
        value (int): the value of the node to search for and delete
        path [(string, int)]: the path and operations taken to perform the
        insertion

    returns (Node, (string, int)):
        the tree in an updated state after the deletion of the node.
        tree will be returned in an identical state if the value
        requested for deletion does not exist.
    """
    #value not found
    if root == None:
        path.append((NOT_FOUND, value))
        return (root, path)

    if root.get_value() < value:
        path.append((SEARCH, root.get_value()))
        root.right, path = h_delete(root.get_right_child(), value, path)
    elif root.get_value() > value:
        path.append((SEARCH, root.get_value()))
        root.left, path = h_delete(root.get_left_child(), value, path)
    else:
        #this is the one to delete
        if root.no_children():
            path.append((DELETE, value))
            root = None
        elif root.one_child():
            child = root.one_child()
            path.append((DELETE, root.get_value()))
            root = child
        else:
            minimum_node = min_node(root.right)
            root_value = root.get_value()
            path.append((SWAP, (root_value, minimum_node.get_value())))
            root.set_value(minimum_node.get_value())
            minimum_node.set_value(root_value)
            root.right, path = h_delete(root.right, root_value, path)
    return (root, path)


def delete(root, value):
    """
    attempts to delete the node with a specified value in the tree

    parameters:
        root (Node): the tree to delete from
        value (int): the value of the node to search for and delete

    returns (Node, [(string, int)], int, int):
        1st value is the new tree (possibly unchanged). 2nd is the operations
        taken to perform this action on the tree. 3rd is height of tree after
        operation. 4th is the level the newly inserted node is located on.
    """
    if root == None:
        return (root, [(NOT_FOUND, value)])

    root, path = h_delete(root, value, [])
    height = get_height(root)
    level = get_level(root, value) 

    return (root, path, height, level)


def h_insert(root, value, path):
    """
    helper function to insert a node into a binary search tree.

    parameters:
        root (Node): the tree to insert into
        value (int): the value to try and insert into the tree
        path [(string, int)]: the path and operations taken to perform the
        insertion

    returns (Node, [(string, int)]):
        the binary search tree with the new node inserted.
        if a duplicate is encountered, the tree will be returned
        in an identical state. second arg is the path and operations taken to 
        perform the insertion.
    """
    if root == None:
        path.append((INSERT, value))
        return (Node(value), path)

    #make no changes if duplicate found
    if root.get_value() == value:
        path.append((DUPLICATE, value))
        return (root, path)

    path.append((SEARCH, root.get_value()))

    if root.get_value() < value:
        root.right, path = h_insert(root.right, value, path)
    elif root.get_value() > value:
        root.left, path = h_insert(root.left, value, path)

    return (root, path)


def insert(root, value, max_height):
    """
    function to insert a node into a binary search tree.

    parameters:
        root (Node): the tree to insert into.
        value (int): the value to try and insert into the tree.
        max_height (int): the maximum tree height allowed by the view

    returns (Node, [(string, int)], int, int):
        1st value is the new tree (possibly unchanged). 2nd is the operations
        taken to perform this action on the tree. 3rd is height of tree after
        operation. 4th is the level the newly inserted node is located on.
    """
    if root == None:
        return (Node(value), [(INSERT, value)], 1, 0)

    root, path = h_insert(root, value, [])

    height = get_height(root)
    level = get_level(root, value)

    if height > max_height:
        root, path, height, level = delete(root, value)
        path = []

    return (root, path, height, level)


def h_search(root, value, path):
    """
    helper function to search the binary search tree for a specified value.

    parameters:
        root (Node): the tree to search
        value (int): the value to try and locate in the tree
        path [(string, int)]: the path and operations taken to perform the
        insertion

    returns ((string, int)...):
        the path taken in performing this search operation on the tree.
    """
    #value can't be found in the tree
    if root == None:
        path.append((NOT_FOUND, value))
        return path

    root_value = root.get_value()

    #determine which node to search next
    if root_value == value:
        path.append((FIND, value))
        return path
    else:
        path.append((SEARCH, root_value))
        if root_value < value:
            return h_search(root.get_right_child(), value, path)
        else:
            return h_search(root.get_left_child(), value, path)


def search(root, value):
    """
    function to search the binary search tree for a specified value

    parameters:
        root (Node): the tree to search
        value (int): the value to try and locate in the tree

    returns (Node, (string, int)):
        the node located with that value if found. none if there was no
        matching node in the binary search tree. second argument is path taken
        to search for the value.
    """
    #value can't be found in the tree
    if root == None:
        return (None, [(NOT_FOUND, value)])

    return (root, h_search(root, value, []))


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


def get_level(root, value):
    """
    given a value in a bst, returns the integer level where the value is found.

    parameters:
        root (Node): the bst to search for the value.
        value (int): the value to be located in the tree.

    returns (int):
        the level that the given node is on in the tree.
    """
    if root == None:
        return -sys.maxsize
    
    if value < root.value:
        return 1 + get_level(root.get_left_child(), value)
    elif value > root.value:
        return 1 + get_level(root.get_right_child(), value)

    return 0


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

def inorder(root):
    """
    perform an inorder traversal of the given binary search tree.

    parameters:
        root (Node): the tree on which the traversal will be performed

    returns ((string, int)):
        the path taken to perform this traversal.
    """
    if root == None:
        return []

    left_list = inorder(root.left)
    middle_value = root.value
    right_list = inorder(root.right)

    
    return left_list + [(SEARCH, middle_value)] + right_list


def preorder(root):
    """
    perform a preorder traversal on a given binary search tree.

    parameters:
        root (Node): the tree on which the traversal will be performed

    returns ((string, int)):
        the path taken to perform this traversal.
    """
    if root == None:
        return []

    middle_value = root.value
    left_list = preorder(root.left)
    right_list = preorder(root.right)

    return [(SEARCH, middle_value)] + left_list + right_list


def postorder(root):    
    """
    perform a postorder traversal on a given binary search tree.

    parameters:
        root (Node): the tree on which the traversal will be performed

    returns ((string, int)):
        the path taken to perform this traversal.
    """
    if root == None:
        return []

    left_list = postorder(root.left)
    right_list = postorder(root.right)
    middle_value = root.value

    return left_list + right_list + [(SEARCH, middle_value)]


def level_values(root, level):
    """
    function to get the value of every node at the requested level.

    parameters:
        root (Node): the binary search tree to get the values for
        level (int): the level to get the values for in the tree

    returns ([int]):
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

    returns ((string, int)):
        the path taken to perform this traversal.
    """
    height = get_height(root)
    node_values = []
    level = 1

    while level <= height:
        node_values += map(lambda value: (SEARCH, value), 
            level_values(root, level))
        level += 1

    return node_values