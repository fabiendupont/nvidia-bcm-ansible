from pythoncm.entity.metadata.cloudregion import CloudRegion


class OCIRegion(CloudRegion):
    def __init__(self):
        super().__init__()
        self.baseType = 'CloudRegion'
        self.childType = 'OCIRegion'
        self.service_type = self.baseType
        self.allTypes = ['OCIRegion', 'CloudRegion']
        self.top_level = True
        self.leaf_entity = True

