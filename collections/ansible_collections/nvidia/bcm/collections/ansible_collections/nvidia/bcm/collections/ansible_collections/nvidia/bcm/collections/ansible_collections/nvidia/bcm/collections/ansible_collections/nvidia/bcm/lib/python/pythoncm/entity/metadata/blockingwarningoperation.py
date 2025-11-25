from pythoncm.entity.metadata.blockingoperation import BlockingOperation


class BlockingWarningOperation(BlockingOperation):
    def __init__(self):
        super().__init__()
        self.baseType = 'BlockingOperation'
        self.childType = 'BlockingWarningOperation'
        self.service_type = self.baseType
        self.allTypes = ['BlockingWarningOperation', 'BlockingOperation']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

