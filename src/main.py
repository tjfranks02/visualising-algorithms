import PySimpleGUI as sg

GRAPH_DIMENSIONS = (500, 500)
GRAPH_DIMENSION = 500


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

    def main_loop(self):
        
        while True:
            
            #await events on the window
            event, values = self.window.read()
            print(event)
            print(values)

            if event in (sg.WIN_CLOSED, 'Cancel'):
                break


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





"""
INITIALISATION CODE FOR WINDOW AND GUI
"""
sg.theme('DarkAmber')   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...

input_layout = [
    [sg.Text("Binary search tree")],
    [sg.OptionMenu(values=("Insert", "Delete", "Search"), default_value="Insert", key="BST_METHOD")],
    [sg.Input(key="BST_ACTION_VAL", enable_events=True), sg.Button("Perform action", enable_events=True, key="BST_TREE_ACTION")]
]

graphing_layout = [
    sg.Graph(
        GRAPH_DIMENSIONS, (0,0), GRAPH_DIMENSIONS,
        background_color="red", 
        key='-GRAPH-', 
        enable_events=True, 
    )
]

layout = input_layout + [graphing_layout]

# Create the Window
window = sg.Window('Window Title', layout, finalize=True)

controller = BSTController(window)
controller.main_loop()

window.close()