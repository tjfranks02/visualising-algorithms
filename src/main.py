import PySimpleGUI as sg

"""
implementation of binary search tree that also returns the actions taken to
perform a certain action.
"""
import bst

"""
class responsible for displaying the tree on the graph.
"""
from bstview import *

"""
identifiers for our gui elements. will also be the name of events that happen
on the elements.
"""
BST_TREE_ACTION = "BST_TREE_ACTION"
BST_GRAPH = "BST_TREE_CANVAS"
BST_METHOD = "BST_METHOD"
BST_ACTION_VAL = "BST_ACTION_VAL"

"""
methods on bst tree
"""
BST_INSERT = "Insert"
BST_DELETE = "Delete"
BST_SEARCH = "Search"
BST_BFS = "BFS"
BST_PREORDER = "Preorder"
BST_POSTORDER = "Postorder"
BST_INORDER = "Inorder"




class BSTController:
    """
    coordinating class enabling communication between view and model for BST.
    """
    def __init__(self, window):
        """
        initialise a controller that aids in displaying a BST

        parameters:
            window (PSG::Window): the window in which to draw the BST
        """
        self.window = window 
        self.view = BSTView(window) #tree display
        self.tree_model = None #underlying search tree data structure


    def validate_input(self, value):
        """
        function to verify whether user-inputted value is in fact valid. the
        value is valid if it can be expressed as an integer.

        parameters:
            value (string): the user input to test for validity.

        returns (Bool):
            true if input valid, false if not.
        """
        try:
            value = int(value)
            return True
        except:
            return False


    def main_loop(self):
        """
        the main loop processing input from window and displaying tree.
        """
        instruction_queue = []
        tree_height = 0
        current_node_level = 0

        while True:
            #await events on the window
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            
            value = values[BST_ACTION_VAL]
            if not self.validate_input(value):
                continue

            #a tree method has been requested
            if event == BST_TREE_ACTION:
                method = values[BST_METHOD]

                if method == BST_INSERT:
                    self.tree_model, instruction_queue, tree_height, \
                        current_node_level = bst.insert(self.tree_model, 
                        int(value), HEIGHT_LIMIT)
                elif method == BST_SEARCH:
                    self.tree_model, instruction_queue = \
                        bst.search(self.tree_model, int(value))
                elif method == BST_DELETE:
                    self.tree_model, instruction_queue, tree_height, \
                        current_node_level = bst.delete(self.tree_model, 
                        int(value))
                elif method == BST_BFS:
                    instruction_queue = bst.breadth_first(self.tree_model)
                elif method == BST_PREORDER:
                    instruction_queue = bst.preorder(self.tree_model)
                elif method == BST_INORDER:
                    instruction_queue = bst.inorder(self.tree_model)
                elif method == BST_POSTORDER:
                    instruction_queue = bst.postorder(self.tree_model)

                self.view.animation_loop(instruction_queue, tree_height, 
                    current_node_level, self.tree_model)




#create the Window
window = sg.Window("Binary search tree")

#controller class to coordinate between view and model
controller = BSTController(window)
controller.main_loop()

#when window has been exited
window.close()