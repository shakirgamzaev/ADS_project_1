

class MaxPairingHeap:
    
    class Node: 
        def __init__(self, key, payload= None):
            self.key = key # holds the python tuple (priority, -submitTime, -flightID)
            self.payload = payload #pointer to flight record 
            self.child: MaxPairingHeap.Node | None = None #pointer to leftmost child
            self.left_sibling: MaxPairingHeap.Node | None = None #pointer to left sibling. If first node in the list of siblings, points to parent, if any parent.
            self.right_sibling: MaxPairingHeap.Node | None = None #pointer to right sibling.
    
    def __init__(self):
        self.root: MaxPairingHeap.Node | None = None # pointer to the root of the
        self.node_count = 0 # counts how many nodes the MaxPairing heap has
    
    def meld(self, node1: Node, node2: Node ) -> Node:
        #base cases, check that both of nodes are not None. even if at least 1 of them is None, immediately return the other one and stop the function call
        if node1 is None:
            return node2
        if node2 is None:
            return node1
        
        #node1 becomes the new root and returned from function
        if node1.key >= node2.key:
            node1_left_most_child = node1.child
            node1.child = node2
            node2.right_sibling = node1_left_most_child
            node2.left_sibling = node1 #setting the left sibling ptr to be the pointer to the parent, which is now node 1
            
            if node1_left_most_child is not None:
                node1_left_most_child.left_sibling = node2
                
            return node1
        else:
            node2_left_child = node2.child
            node2.child = node1 # node1, since smaller or equal, becomes the new leftmost child of node 2
            node1.right_sibling = node2_left_child
            node1.left_sibling = node2 #rewire so that left ptr points to node2, new parent
            
            if node2_left_child is not None:
                node2_left_child.left_sibling = node1
                
            return node2
        
        
        
    # helper function for increaseKey operation that detaches a specific node from its sibling list
    def detach_node(self, node: Node):
        
        #if the node is the leftmost child of the parent
        if node.left_sibling is not None and node.left_sibling.child == node:
            parent_node = node.left_sibling
            node_right_sibling = node.right_sibling
            parent_node.child = node_right_sibling
            
            if node_right_sibling is not None:
                node_right_sibling.left_sibling = parent_node
        
        else:
            node_left_sibling = node.left_sibling
            node_right_sibling = node.right_sibling
            #rewire sibling pointers of the right and left siblings of the current node that is to be detached. Of course as a safety check to see whether the left siblings are not None
            
            if node_left_sibling is not None:
                node_left_sibling.right_sibling = node_right_sibling
                
            if node_right_sibling is not None:
                node_right_sibling.left_sibling = node_left_sibling
        
        #clear the left and right sibling pointers
        node.left_sibling = None
        node.right_sibling = None
        
    
    
    #helper function that performs 2-pass merge scheme
    def two_pass_merge(self, node: Node) -> Node | None:
        if node is None:
            return None
        
        #Pass 1: merge pairwise
        merged_pairs: list[MaxPairingHeap.Node] = []
        current_node_ptr: MaxPairingHeap.Node | None = node #pointer to the current node in the list of siblings
        
        while current_node_ptr is not None:
            #an odd unpaired, the last remaning one that was not merged
            if current_node_ptr.right_sibling is None:
                #if the merged_pairs is empty, it means that this node is the only one so just append it to merged_pairs and break out of while loop
                if len(merged_pairs) == 0:
                    merged_pairs.append(current_node_ptr)
                else:
                    #get the last node from merged_pairs and meld it with the remaining one
                    last_node = merged_pairs.pop()
                    new_node = self.meld(last_node, current_node_ptr)
                    merged_pairs.append(new_node)
                break
            else:
               right_sibling = current_node_ptr.right_sibling
               next_node = right_sibling.right_sibling
               
               #detach a pair of nodes from the main list of siblings before melding
               current_node_ptr.right_sibling = None
               right_sibling.left_sibling = None
               
               new_merged_node = self.meld(current_node_ptr, right_sibling)
               merged_pairs.append(new_merged_node)
               current_node_ptr = next_node
               
        #Pass 2: merge into one pairing heap starting from the rightmost node
        result = merged_pairs.pop()
        while len(merged_pairs) > 0:
            right_most_node = merged_pairs.pop()
            result = self.meld(result, right_most_node)
        return result
                    
    
    
    #inserts a new node with given key priority, which a tuple
    def push(self, key, payload=None) -> Node:
        new_node = MaxPairingHeap.Node(key, payload)
        self.root = self.meld(new_node, self.root)
        self.node_count += 1
        return new_node
    
    
    
    def increase_key(self, node: Node, new_key):
        #if node is root, then do nothing except increase the
        if node == self.root:
            self.root.key = new_key
            return
        #else, increase node key, detach it from the sibling list, and re meld with the root 
        node.key = new_key
        self.detach_node(node)
        self.root = self.meld(node, self.root)
    
    def erase(self, node: Node): 
        if node is None:
            return
        #special case, if removing a root node, then call pop
        if node == self.root:
            self.pop()
            return

        self.detach_node(node)
        #if the node has chidren, use 2 pass merge scheme to meld them, and then meld with the original root
        if node.child is not None:
            node.child.left_sibling = None
            merged_children = self.two_pass_merge(node.child)
            self.root = self.meld(self.root, merged_children)
        
        node.child = None
        self.node_count -= 1
        
    
    #removes the max element from the heap, and uses 2-pass merge scheme to merge children of root, if any
    def pop(self) -> Node | None:
        #Fail case: if the root node is None, meaning the heap is empty, do nothing and simply return None
        if self.root is None:
            return None
        #1) detach root from the heap
        root = self.root
        
        # if root does not have any children then just return it and make heap empty
        if root.child is None:
            self.root = None
            self.node_count -= 1
            return root
        else:
            root.child.left_sibling = None
            self.root = self.two_pass_merge(root.child)
            root.child = None
            self.node_count -= 1
            return root
