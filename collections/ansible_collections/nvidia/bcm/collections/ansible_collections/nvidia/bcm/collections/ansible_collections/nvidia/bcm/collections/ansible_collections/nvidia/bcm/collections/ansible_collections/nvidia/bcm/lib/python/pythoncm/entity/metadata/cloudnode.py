from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.computenode import ComputeNode


class CloudNode(ComputeNode):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="cloudSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing all cloud node settings",
                instance='CloudSettings',
                init_instance='EC2Settings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'Device'
        self.childType = 'CloudNode'
        self.service_type = self.baseType
        self.allTypes = ['CloudNode', 'ComputeNode', 'Node', 'Device']
        self.top_level = True
        self.leaf_entity = True

