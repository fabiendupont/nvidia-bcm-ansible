from pythoncm.entity.metadata.computenode import ComputeNode


class PhysicalNode(ComputeNode):
    """
    Node
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'Device'
        self.childType = 'PhysicalNode'
        self.service_type = self.baseType
        self.allTypes = ['PhysicalNode', 'ComputeNode', 'Node', 'Device']
        self.top_level = True
        self.leaf_entity = True

