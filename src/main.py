import PySimpleGUI as sg
import math

import bst

"""
configuration for gui elements
"""
GRAPH_DIMENSIONS = (500, 500)
GRAPH_DIMENSION = 500
NODE_RADIUS = 20
ROOT_COORDS = (int(GRAPH_DIMENSION / 2), GRAPH_DIMENSION - 50)

BACKGROUND_COLOUR = "snow"
TEXT_COLOUR = "snow"
NEUTRAL_COLOUR = "lime green"
VISITED_COLOUR = "firebrick2"
NEW_INSERT_COLOUR = "purple4"
THEME = "DarkBlue"

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
            if event == BST_TREE_ACTION and not animating:
                
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
            btm_rgt_line=None, x_coord=None, y_coord=None, radius=NODE_RADIUS):
        self.node_id = node_id
        self.text_id = text_id
        self.top_line = top_line
        self.btm_lft_line = btm_lft_line
        self.btm_rgt_line = btm_rgt_line
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.radius = radius

    """
    getters and setters
    """
    def get_btm_rgt_coords(self):
        """
        calculate the coordinates on the bottom right of the node where a line 
        should be connected.
        """
        x_coord = self.x_coord + (self.radius / 2)
        y_coord = -math.sqrt((self.radius ** 2) - 
            (x_coord - self.x_coord) ** 2) + self.y_coord
        return (x_coord, y_coord)

    def get_btm_lft_coords(self):
        """
        calculate the coordinates on the bottom left of the node where a line 
        should be connected.
        """
        x_coord = self.x_coord - (self.radius / 2)
        y_coord = -math.sqrt((self.radius ** 2) -
            (x_coord - self.x_coord) ** 2) + self.y_coord
        return (x_coord, y_coord)

    def get_top_coords(self):
        """
        calculate the coordinates on the top of the node where a line should be
        connected.
        """
        x_coord = self.x_coord
        y_coord = self.y_coord + self.radius
        return (x_coord, y_coord)

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
                fill_color=NEUTRAL_COLOUR, radius=20)
            
            text_id = self.graph.draw_text(node_value, coords, 
                color=TEXT_COLOUR)

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
        instruction = current[0]

        if instruction == FIND:
            pass
        elif instruction == SEARCH:
            self.animate_search(current)
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
    

    def animate_search(self, new_instruction):
        """
        function to display an animation of searching a node on the tree.

        parameters:
            new_instruction ((string, int)): the current instruction to be 
                executed. int is the value to search for.
        """
        search_val = new_instruction[1]
        search_node = self.tree_vals[search_val]
        coords = search_node.get_coords()

        node_id = self.graph.draw_circle(coords,
            fill_color=VISITED_COLOUR, radius=20)
        text_id = self.graph.draw_text(search_val, coords, color=TEXT_COLOUR)
        self.tree_vals[search_val] = BSTNode(node_id, text_id, 
            x_coord=coords[0], y_coord=coords[1])
        self.redraw.append(search_val)


    def animate_insert(self, prev_instruction, new_instruction, height, level):
        """
        function to animate the insertion of a node on the tree.

        parameters:
            prev_instruction ((string, int)): the previous instruction executed 
                int part is relevant for this function, representing the node 
                value acted upon in the previous instruction.
            new_instruction ((string, int)): the current instruction to be 
                executed. int is the value to insert. 
            height (int): the height of the tree after the insertion
            level (int): the level that the new node is located at
        """
        prev_val = None
        new_val = new_instruction[1]

        print("previous instruction:", prev_instruction)
        print("current instruction:", new_instruction)

        #the tree is not empty
        if prev_instruction != None:
            new_x = 0
            new_y = 0
            
            prev_val = prev_instruction[1]
            prev_node = self.tree_vals[prev_val]

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
        self.draw_node(new_x, new_y, new_val, prev_val, NEW_INSERT_COLOUR)


    def draw_node(self, x_coord, y_coord, new_val, connecting_val, node_colour):
        """
        when a node insertion is triggered, this function will draw the shapes
        upon the graph element.

        parameters:
            x_coord, y_coord (int): x and y coords
            new_val (string): the new value to insert into the node
            connecting_val (string): the value of the node connected to the
                newly inserted node
        """
        connecting_node = self.tree_vals.get(connecting_val)

        node_id = self.graph.draw_circle((x_coord, y_coord),
            fill_color=node_colour, radius=20)
        text_id = self.graph.draw_text(new_val, (x_coord, y_coord), 
            color=TEXT_COLOUR)
        self.tree_vals[new_val] = BSTNode(node_id, text_id, x_coord=x_coord, 
                y_coord=y_coord)
        self.redraw.append(new_val)

        #if a line is required to be drawn
        line_id = None

        if connecting_val != None:
            up_coords = connecting_node.get_btm_lft_coords()
            down_coords = self.tree_vals[new_val].get_top_coords()

            print("connection to top:", up_coords)
            print("connection to node:", down_coords)

            if connecting_val < new_val:
                up_coords = connecting_node.get_btm_rgt_coords()

            line_id = self.graph.draw_line(down_coords, up_coords)

        
"""
INITIALISATION CODE FOR WINDOW AND GUI
"""
sg.theme(THEME)   # Add a little color to your windows
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
        background_color=BACKGROUND_COLOUR, 
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