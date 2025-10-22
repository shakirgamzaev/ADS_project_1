# pylint: disable=missing-class-docstring
# pylint: disable=trailing-whitespace
#pylint: disable=missing-function-docstring


class MinHeap:
    """min heap implementation"""
    
    class Node:
        def __init__(self, key, payload = None):
            self.key = key
            self.payload = payload
    
    def __init__(self) -> None:
        self.nodes: list[MinHeap.Node] = []
        
    
    def insert_node(self, node: Node):
        self.nodes.append(node)
        index_last_node = len(self.nodes) - 1
        self.bubble_up(index_last_node)
          
    
    def print_heap(self):
        for i in self.nodes:
            print(i.key)
    
    #returns the minimum node without removing it from the heap
    def peek_min(self) -> Node | None:
        if len(self.nodes) == 0:
            return None
        return self.nodes[0]
    
    def remove_min(self) -> Node | None:
        # since empty, dont return None, so no node
        if len(self.nodes) == 0:
            return None
        #if only 1 node available, return it form list
        elif len(self.nodes) == 1:
            return self.nodes.pop()
        min_node = self.nodes[0]
        last_node = self.nodes.pop()
        self.nodes[0] = last_node
        self.bubble_down(0)
        
        return min_node
        
    def bubble_up(self, index: int) -> None:
        current_index = index
        while current_index > 0:
            parent_index = (current_index - 1) // 2
            if self.nodes[current_index].key >= self.nodes[parent_index].key:
                break
            else:
                self.swap_nodes(current_index, parent_index)
                current_index = parent_index #update so that new cur index is the parent 
    
    
    def bubble_down(self, index: int) -> None:
        left_index = (index * 2) + 1
        right_index = (index * 2) + 2
        smallest = index #keeps track whether index changed to either of its children
        
        if left_index < len(self.nodes) and self.nodes[left_index].key < self.nodes[smallest].key:
            smallest = left_index
        if right_index < len(self.nodes) and self.nodes[right_index].key < self.nodes[smallest].key:
            smallest = right_index
        
        if index != smallest:
            self.swap_nodes(smallest, index)
            self.bubble_down(smallest)
        
        
    # swap nodes by indices
    def swap_nodes(self, index1: int, index2: int):
        temp_node = self.nodes[index1]
        self.nodes[index1] = self.nodes[index2]
        self.nodes[index2] = temp_node