import PySimpleGUI as sg

import bst

"""
configuration for gui elements
"""
GRAPH_DIMENSIONS = (500, 500)
GRAPH_DIMENSION = 500

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
        self.view = BSTView(window[BST_GRAPH]) #class handling tree display
        self.tree_model = None

    def main_loop(self):
        
        while True:
            
            #await events on the window
            event, values = self.window.read()
            print(event)
            print(values)

            if event == sg.WIN_CLOSED:
                break

            if event == BST_TREE_ACTION:
                method = values[BST_METHOD]
                value = values[BST_ACTION_VAL]

                if method == BST_INSERT:
                    self.insert_node(value)
                elif method == BST_DELETE:
                    self.delete_node(value)
                else:
                    self.search_tree(value)
                    
    def insert_node(self, value):

        if self.tree_model == None:
            self.tree_model = bst.create(value)
        else:
            self.tree_model = bst.insert(self.tree_model, value)
    
    def delete_node(self, value):
        if self.tree_model != None:
            self.tree_model = bst.delete(self.tree_model, value)

    def search_tree(self, value):
        
        if self.tree_model != None:
            node = bst.search(self.tree_model, value)



class BSTNode:

    def __init__(self, graph, top_line=None, btm_lft_line=None, 
            btm_rgt_line=None):
        self.top_line = top_line
        self.btm_lft_line = btm_lft_line
        self.btm_rgt_line = btm_rgt_line

class BSTView:
    """
    this is a class capable of displaying a binary search tree upon a PSG graph
    element and performing various animations to display the process of
    performing various actions on the tree.
    """

    def __init__(self, graph):
        """
        initialise the view of the BST

        parameters:
            graph (PSG::Graph): the graph element to display the tree on
        """
        self.graph = graph

    def insert_node(self, graph):
        """
        this one will need to 
        """
        pass





"""
INITIALISATION CODE FOR WINDOW AND GUI
"""
sg.theme('DarkAmber')   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...

input_layout = [
    [sg.Text("Binary search tree")],
    [sg.OptionMenu(values=(BST_INSERT, BST_DELETE, BST_SEARCH), default_value=BST_INSERT, key=BST_METHOD)],
    [sg.Input(key=BST_ACTION_VAL, enable_events=True), sg.Button("Perform action", enable_events=True, key=BST_TREE_ACTION)]
]

graphing_layout = [
    sg.Graph(
        GRAPH_DIMENSIONS, (0,0), GRAPH_DIMENSIONS,
        background_color="red", 
        key=BST_GRAPH, 
        enable_events=True 
    )
]

layout = input_layout + [graphing_layout]

# Create the Window
window = sg.Window('Window Title', layout, finalize=True)

controller = BSTController(window)
controller.main_loop()

window.close()