from pythoncm.entity.metadata.role import Role


class CloudGatewayRole(Role):
    def __init__(self):
        super().__init__()
        self.baseType = 'Role'
        self.childType = 'CloudGatewayRole'
        self.service_type = self.baseType
        self.allTypes = ['CloudGatewayRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

