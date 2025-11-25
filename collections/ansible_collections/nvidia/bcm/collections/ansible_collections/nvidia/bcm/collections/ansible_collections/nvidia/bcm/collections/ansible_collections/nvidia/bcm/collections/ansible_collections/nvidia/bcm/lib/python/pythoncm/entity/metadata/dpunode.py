from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.computenode import ComputeNode


class DPUNode(ComputeNode):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="dpuSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing all DPU node settings",
                instance='DPUSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostNode",
                kind=MetaData.Type.RESOLVE,
                description="Host node",
                instance='Node',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'Device'
        self.childType = 'DPUNode'
        self.service_type = self.baseType
        self.allTypes = ['DPUNode', 'ComputeNode', 'Node', 'Device']
        self.top_level = True
        self.leaf_entity = True

