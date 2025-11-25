from pythoncm.entity.metadata.node import Node


class HeadNode(Node):
    """
    Head node
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'Device'
        self.childType = 'HeadNode'
        self.service_type = self.baseType
        self.allTypes = ['HeadNode', 'Node', 'Device']
        self.top_level = True
        self.leaf_entity = True

