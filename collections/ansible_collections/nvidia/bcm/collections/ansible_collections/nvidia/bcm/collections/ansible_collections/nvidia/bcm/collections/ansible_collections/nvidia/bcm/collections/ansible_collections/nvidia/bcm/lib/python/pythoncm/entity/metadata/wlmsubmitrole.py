from pythoncm.entity.metadata.role import Role


class WlmSubmitRole(Role):
    """
    WLM submit role
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'Role'
        self.childType = 'WlmSubmitRole'
        self.service_type = self.baseType
        self.allTypes = ['WlmSubmitRole', 'Role']
        self.leaf_entity = False

