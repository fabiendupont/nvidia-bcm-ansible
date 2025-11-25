from pythoncm.entity.metadata.cloudregion import CloudRegion


class GCPZone(CloudRegion):
    def __init__(self):
        super().__init__()
        self.baseType = 'CloudRegion'
        self.childType = 'GCPZone'
        self.service_type = self.baseType
        self.allTypes = ['GCPZone', 'CloudRegion']
        self.top_level = True
        self.leaf_entity = True

