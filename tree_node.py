
class Node:
    def __init__(self, value=None, node_type=None):
        self.value = value
        self.children = []
        self.node_type = node_type   
        self.ispruned = False        
        self.probability = []        
        self.move = None             
        self.alpha = None            
        self.beta = None

    def add_child(self, child, prob=None):
        self.children.append(child)
        self.probability.append(prob)
