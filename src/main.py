import PySimpleGUI as sg
import math

import bst

"""
configuration for gui elements
"""
GRAPH_DIMENSIONS = (500, 500)
GRAPH_DIMENSION = 500
NODE_RADIUS = 19
GRAPH_BORDER = 50
GRAPH_DRAWABLE_DIMENSIONS = (GRAPH_DIMENSION - 2 * GRAPH_BORDER, 
    GRAPH_DIMENSION - 2 * GRAPH_BORDER)
ROOT_COORDS = (((GRAPH_DIMENSION - 2 * GRAPH_BORDER) / 2) + GRAPH_BORDER, 
    GRAPH_DIMENSION - GRAPH_BORDER)

HEIGHT_LIMIT = 5
NODE_Y_GAP = GRAPH_DRAWABLE_DIMENSIONS[0] / (HEIGHT_LIMIT - 1)

BACKGROUND_COLOUR = "snow"
TEXT_COLOUR = "snow"
NEUTRAL_COLOUR = "lime green"
VISITED_COLOUR = "firebrick2"
NEW_INSERT_COLOUR = "purple4"
FOUND_NODE_COLOUR = "blue"
THEME = "DarkBlue"
NODE_SWAP_COLOUR = "goldenrod2"
NODE_DUP_COLOUR = "midnight blue"

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
        current_node_level = 0

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
                    tree_height, current_node_level)
                prev_instruction = instruction_queue.pop(0)

            #a tree method has been requested
            if event == BST_TREE_ACTION and not animating:
                
                animating = True
                value = values[BST_ACTION_VAL]
                method = values[BST_METHOD]

                if method == BST_INSERT:
                    self.tree_model, instruction_queue, height, \
                        current_node_level = bst.insert(self.tree_model, 
                        int(value))
                elif method == BST_SEARCH:
                    self.tree_model, instruction_queue = \
                        bst.search(self.tree_model, int(value))


class BSTNode:
    """
    a class describing a node positioned on the graph element. includes
    coordinates as well as lines connecting nodes.
    """
    def __init__(self, node_id, text_id, x_coord=None, 
            y_coord=None, radius=NODE_RADIUS):
        """
        parameters:
            node_id (int): the pysimplegui id returned from calling 
                create_circle.
            text_id (int): the pysimplegui id returned from calling create_text
            x_coord, y_coord (int): coordinates for the center of this node on 
                the graph.
            radius (int): the radius of this node on the graph.
        """
        self.node_id = node_id
        self.text_id = text_id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.radius = radius
        self.level = 0

    """
    getters and setters
    """
    def get_btm_rgt_coords(self):
        """
        returns (int, int):
            the coordinates where a line should be connected on the bottom right 
            of this node.
        """
        x_coord = self.x_coord + (self.radius / 2)
        y_coord = -math.sqrt((self.radius ** 2) - 
            (x_coord - self.x_coord) ** 2) + self.y_coord
        return (x_coord, y_coord)

    def get_btm_lft_coords(self):
        """
        returns (int, int):
            the coordinates where a line should be connected on the bottom left 
            of this node.
        """
        x_coord = self.x_coord - (self.radius / 2)
        y_coord = -math.sqrt((self.radius ** 2) -
            (x_coord - self.x_coord) ** 2) + self.y_coord
        return (x_coord, y_coord)

    def get_top_coords(self):
        """
        returns (int, int):
            the coordinates where a line should be connected on the top of this 
            node.
        """
        x_coord = self.x_coord
        y_coord = self.y_coord + self.radius
        return (x_coord, y_coord)

    def get_coords(self):
        return (self.x_coord, self.y_coord)
    
    def set_coords(self, coords):
        self.x_coord = coords[0]
        self.y_coord = coords[1]

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level


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
        redraws the nodes that have been involved in an animation. the list of
        nodes is stored in self.redraw.
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
                fill_color=NEUTRAL_COLOUR, radius=node.radius)
            
            text_id = self.graph.draw_text(node_value, coords, 
                color=TEXT_COLOUR)

            self.redraw = []
        

    def animate_path(self, previous, current, height, level):
        """
        takes an instruction generated during a bst operation and animates it
        for the user's benefit.

        parameters:
            previous (string, int): the previous instruction executed
            current (string, int): the new instruction to execute
            height (int): the height of the tree
            level (int): the level at which the node being acted upon is located
                in the NEW representation of the tree. e.g. if searching, what
                level of the tree was the node found at.
        """
        instruction = current[0]

        if instruction == FIND:
            self.animate_access(current, FOUND_NODE_COLOUR)
        elif instruction == SEARCH:
            self.animate_access(current, VISITED_COLOUR)
        elif instruction == SWAP:
            self.animate_swap(current)
        elif instruction == INSERT:
            self.animate_insert(previous, current, height, level)
        elif instruction == NOT_FOUND:
            pass
        elif instruction == DUPLICATE:
            self.animate_access(current, NODE_DUP_COLOUR)
        elif instruction == DELETE:
            pass
        elif instruction == RESTRUCTURE:
            pass

    def animate_swap(self, new_instruction):
        """
        when deleting, node values sometimes need to be swapped. this function 
        animates that process.

        parameters:
            new_instruction (string, (int, int)): the new instruction to
                process. the string is simply the name of the instruction and
                the two ints are the values to swap on the tree.
        """
        swap_vals = new_instruction[1]
        node1 = self.tree_vals[swap_vals[0]]
        node2 = self.tree_vals[swap_vals[1]]

        node1_coords = node1.get_coords()
        node2_coords = node2.get_coords()

        self.draw_node(node1_coords[0], node1_coords[1], node2.value, 
            None, NODE_SWAP_COLOUR, 2 * node1.radius)
        self.draw_node(node2_coords[0], node2_coords[1], node1.value, 
            None, NODE_SWAP_COLOUR, 2 * node2.radius)

        self.redraw.append(swap_vals[0])
        self.redraw.append(swap_vals[1])

        self.tree_vals[swap_vals[0]] = node2
        self.tree_vals[swap_vals[1]] = node1

    def animate_access(self, new_instruction, colour):
        """
        function to display an animation of accessing a node on the tree. 

        parameters:
            new_instruction ((string, int)): the current instruction to be 
                executed. int is the value to search for.
            colour (string): the node could be part of a search path or could be
                the value being searched for. each has a different colour.
        """
        search_val = new_instruction[1]
        search_node = self.tree_vals[search_val]
        coords = search_node.get_coords()

        x_space = GRAPH_DRAWABLE_DIMENSIONS[0] / (2 * (2 ** search_node.level))

        self.draw_node(coords[0], coords[1], search_val, None, 
            colour, x_space)


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
        x_offset = GRAPH_DRAWABLE_DIMENSIONS[0] / (2 * (2 ** level))

        #the tree is not empty
        if prev_instruction != None:
            new_x = 0
            new_y = 0

            prev_val = prev_instruction[1]
            prev_node = self.tree_vals[prev_val]

            if prev_val > new_val:
                new_x = prev_node.x_coord - x_offset
                new_y = prev_node.y_coord - NODE_Y_GAP
            else:
                new_x = prev_node.x_coord + x_offset
                new_y = prev_node.y_coord - NODE_Y_GAP
        
        #tree empty, add root element
        else:
            new_x = ROOT_COORDS[0]
            new_y = ROOT_COORDS[1]

        #draw necessary shapes on graph
        self.draw_node(new_x, new_y, new_val, prev_val, 
            NEW_INSERT_COLOUR, x_offset)
        self.tree_vals[new_val].level = level


    def draw_node(self, x_coord, y_coord, new_val, connecting_val, 
        node_colour, x_space):
        """
        when a node insertion is triggered, this function will draw the shapes
        upon the graph element.

        parameters:
            x_coord, y_coord (int): x and y coords
            new_val (string): the new value to insert into the node
            connecting_val (string): the value of the node connected to the
                newly inserted node
            node_colour (string): bst nodes can have one of many colours to 
                represent their current state. this is where the 
                colour is specified
            x_space (int): the space along the x-axis that is available to the
                node for drawing. node may need resizing to fit the available
                space.
        """
        connecting_node = self.tree_vals.get(connecting_val)

        radius = min(NODE_RADIUS, x_space)

        node_id = self.graph.draw_circle((x_coord, y_coord),
            fill_color=node_colour, radius=radius)
        text_id = self.graph.draw_text(new_val, (x_coord, y_coord), 
            color=TEXT_COLOUR)
        self.tree_vals[new_val] = BSTNode(node_id, text_id, x_coord=x_coord, 
                y_coord=y_coord, radius=radius)
        self.redraw.append(new_val)

        #if a line is required to be drawn between nodes
        if connecting_val != None:
            up_coords = connecting_node.get_btm_lft_coords()
            down_coords = self.tree_vals[new_val].get_top_coords()

            if connecting_val < new_val:
                up_coords = connecting_node.get_btm_rgt_coords()

            self.graph.draw_line(down_coords, up_coords)








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
graph = window[BST_GRAPH]
graph.draw_line((0, 50), (500, 50))
graph.draw_line((0, 450), (500, 450))
graph.draw_line((50, 0), (50, 500))
graph.draw_line((450, 0), (450, 500))

y_value = NODE_Y_GAP

for num in range(0, HEIGHT_LIMIT + 1):
    graph.draw_line((0, 50 + num * y_value), (500, 50 + num * y_value))

controller = BSTController(window)
controller.main_loop()

window.close()