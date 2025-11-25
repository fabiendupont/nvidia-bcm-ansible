from pythoncm.entity.metadata.osclouddisk import OSCloudDisk


class OSCloudSwapDisk(OSCloudDisk):
    def __init__(self):
        super().__init__()
        self.baseType = 'OSCloudDisk'
        self.childType = 'OSCloudSwapDisk'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudSwapDisk', 'OSCloudDisk']
        self.top_level = False
        self.leaf_entity = True

