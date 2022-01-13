"""
for node at rank i:
    left child is at rank 2i + 1
    right child is at rank 2i + 2
"""
import math

class BinHeap:  

    def __init__(self):
        self.heap = []

    def get_height(self):
        """
        function to get the height of the heap if respresented
        in tree form.

        returns (int):
            the height of the heap represented as a tree.
        """
        return math.floor(math.log(len(self.heap), 2)) + 1

    def upheap(self):
        """
        function performed after every insertion to the heap.
        restores the heap-order property.
        """
        current_index = len(self.heap) - 1
        takeaway = 0

        while True:

            #how much to take away to find parent
            if current_index % 2 == 0:
                takeaway = 2
            else:
                takeaway = 1
            
            #the parent of the current index
            parent_index = max(int((current_index - takeaway) / 2), 0)

            #examine the values at parent and child, possibly switch 
            parent_value = self.heap[parent_index]
            current_value = self.heap[current_index]

            if current_value < parent_value:
                self.heap[parent_index] = current_value
                self.heap[current_index] = parent_value
            else:
                return True
            
            current_index = parent_index
      
    def insert(self, value):
        """
        insert a new value into the heap structure.

        parameters:
            value (int): the new value to insert
        """
        self.heap.append(value)
        self.upheap()
        print(self.heap)

    def downheap(self):
        """
        for node at rank i:
            left child is at rank 2i + 1
            right child is at rank 2i + 2
        """
        parent_index = 0
        index_to_examine = 0

        while True:
            #determine which child index to examine
            left_child_index = 2 * parent_index + 1
            right_child_index = 2 * parent_index + 2

            if self.heap[right_child_index] != None and \
                self.heap[right_child_index] < self.heap[left_child_index]:
                index_to_examine = right_child_index
            else:
                index_to_examine = left_child_index

            #switch if necessary
            examine_value = self.heap[index_to_examine]
            parent_value = self.heap[parent_index]

            if parent_value > examine_value:
                self.heap[parent_index] = parent_value
                self.heap[index_to_examine] = examine_value

            parent_index = index_to_examine
                            
        


    def remove_min(self, value):
        """
        """
        if len(self.heap) == None:
            return False

        #make last element first one
        self.heap[0] = self.heap[len(self.heap) - 1]

        self.downheap()
        

heap = BinHeap()

heap.insert(3)
heap.insert(4)
heap.insert(6)
heap.insert(2)
heap.insert(1)


        