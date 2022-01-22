import PySimpleGUI as sg
import time

import bst

"""
configuration for gui elements
"""
GRAPH_DIMENSIONS = (500, 500)
GRAPH_DIMENSION = 500
CIRCLE_RADIUS = int(GRAPH_DIMENSION * 0.1)
ROOT_COORDS = (int(GRAPH_DIMENSION / 2), GRAPH_DIMENSION - CIRCLE_RADIUS)

"""
identifiers for our gui elements. will also be the name of events that happen
on the elements.
"""
BST_TREE_ACTION = "BST_TREE_ACTION"
BST_GRAPH = "BST_TREE_CANVAS"
BST_METHOD = "BST_METHOD"
BST_ACTION_VAL = "BST_ACTION_VAL"
BST_FORWARD = "BST_FORWARD"

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


def print_tree(root):
    """
    """
    if root == None:
        return

    print("root:", root.get_value())
    
    if root.left != None:
        print("left:", root.left.get_value())
    else:
        print("left: None")

    if root.right != None:
        print("right:", root.right.get_value())
    else:
        print("right: None")

    print("------------------------------")
    print_tree(root.left)
    print_tree(root.right)
    

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
        """
        the main loop processing input from window and displaying tree.
        """
        instruction_queue = []
        prev_instruction = None
        animating = False
        tree_height = -1

        while True:
            #await events on the window
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            
            #user requests next step in animation
            if event == BST_FORWARD and animating:

                if len(instruction_queue) == 0:
                    animating = False
                    self.view.redraw_nodes()
                    continue

                self.view.animate_path(prev_instruction, instruction_queue[0], 
                    tree_height, 0)
                prev_instruction = instruction_queue.pop(0)

            #a tree method has been requested
            if event == BST_TREE_ACTION:
                
                value = values[BST_ACTION_VAL]
                method = values[BST_METHOD]

                if method == BST_INSERT:
                    self.tree_model, path, height, level = bst.insert(
                        self.tree_model, int(value))
                    instruction_queue = path
                    print(instruction_queue)
                    animating = True
                    
            

          
    def remove_items(self, items):
        """
        """
        for item in items:
            self.graph.delete_figure(item)



class BSTNode:
    """
    a class describing a node positioned on the graph element. includes
    coordinates as well as lines connecting nodes.
    """
    def __init__(self, node_id, text_id, top_line=None, btm_lft_line=None, 
            btm_rgt_line=None, x_coord=None, y_coord=None):
        self.node_id = node_id
        self.text_id = text_id
        self.top_line = top_line
        self.btm_lft_line = btm_lft_line
        self.btm_rgt_line = btm_rgt_line
        self.x_coord = x_coord
        self.y_coord = y_coord

    def get_coords(self):
        return (self.x_coord, self.y_coord)
    
    def set_coords(self, coords):
        self.x_coord = coords[0]
        self.y_coord = coords[1]

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
        self.tree_vals = {}
        self.redraw = [] #list of nodes queued to redraw

    def redraw_nodes(self):
        """
        redraws nodes that have been highlighted in the default colour.
        """
        for node_value in self.redraw:
            node = self.tree_vals[node_value]
            node_id = node.node_id
            text_id = node.text_id
            
            #delete the old figures
            self.graph.delete_figure(node_id)
            self.graph.delete_figure(text_id)

            #redraw figures with default colour
            coords = node.get_coords()
            node_id = self.graph.draw_circle(coords,
                fill_color="yellow", radius=20)
            
            text_id = self.graph.draw_text(node_value, coords)

            self.redraw = []
        

    def animate_path(self, previous, current, height, level):
        """
        takes a path returned from a bst and animate the process, displaying it
        on the graph.

        FIND = "FIND"
        SEARCH = "SEARCH"
        SWAP = "SWAP"
        INSERT = "INSERT"
        NOT_FOUND = "NOT_FOUND"
        DUPLICATE = "DUPLICATE"
        DELETE = "DELETE"
        RESTRUCTURE = "RESTRUCTURE"
        """
        prev_instruction = None

        if previous != None:
            prev_instruction = previous[0]

        instruction = current[0]

        if instruction == FIND:
            pass
        elif instruction == SEARCH:
            pass
        elif instruction == SWAP:
            pass
        elif instruction == INSERT:
            self.animate_insert(previous, current, height, level)
        elif instruction == NOT_FOUND:
            pass
        elif instruction == DUPLICATE:
            pass
        elif instruction == DELETE:
            pass
        elif instruction == RESTRUCTURE:
            pass
        
        prev_instruction = instruction


    def animate_insert(self, prev_instruction, new_instruction, height, level):
        """
        function to display an animation of displaying an insertion of a node.

        parameters:
            prev_instruction ((string, int)):
            new_instruction ((string, int)):
            height (int): the height of the tree after the insertion
            level (int): the level that the new node is located at
        """
        prev_val = None
        new_val = new_instruction[1]

        print("previous instruction:", prev_instruction)
        print("current instruction:", new_instruction)

        #the tree is not empty
        if prev_instruction != None:
            prev_val = prev_instruction[1]
            prev_node = self.tree_vals[prev_val]

            new_x = 0
            new_y = 0

            if prev_val > new_val:
                new_x = prev_node.x_coord - 50
                new_y = prev_node.y_coord - 50
            else:
                new_x = prev_node.x_coord + 50
                new_y = prev_node.y_coord - 50
        
        #tree empty, add root element
        else:
            new_x = ROOT_COORDS[0]
            new_y = ROOT_COORDS[1]

        #draw necessary shapes on graph
        node_id = self.graph.draw_circle((new_x, new_y),
            fill_color="green", radius=20)
        text_id = self.graph.draw_text(new_val, (new_x, new_y))
        self.tree_vals[new_val] = BSTNode(node_id, text_id, x_coord=new_x, 
                y_coord=new_y)
        self.redraw.append(new_val)

        print(new_x, new_y)

        
"""
INITIALISATION CODE FOR WINDOW AND GUI
"""
sg.theme('DarkAmber')   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...

input_layout = [
    [sg.Text("Binary search tree")],
    [sg.OptionMenu(values=(BST_INSERT, BST_DELETE, BST_SEARCH), default_value=BST_INSERT, key=BST_METHOD)],
    [sg.Input(key=BST_ACTION_VAL, enable_events=True), sg.Button("Perform action", enable_events=True, key=BST_TREE_ACTION)],
    [sg.Button("Next", key=BST_FORWARD, enable_events=True)]
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
window = sg.Window('Binary Search Tree', layout, finalize=True)

controller = BSTController(window)
controller.main_loop()

window.close()