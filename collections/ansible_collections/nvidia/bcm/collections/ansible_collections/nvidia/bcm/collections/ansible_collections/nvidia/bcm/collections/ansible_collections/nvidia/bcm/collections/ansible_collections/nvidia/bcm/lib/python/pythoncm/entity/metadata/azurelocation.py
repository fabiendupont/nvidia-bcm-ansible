from pythoncm.entity.metadata.cloudregion import CloudRegion


class AzureLocation(CloudRegion):
    def __init__(self):
        super().__init__()
        self.baseType = 'CloudRegion'
        self.childType = 'AzureLocation'
        self.service_type = self.baseType
        self.allTypes = ['AzureLocation', 'CloudRegion']
        self.top_level = True
        self.leaf_entity = True

