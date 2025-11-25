from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeNodeLoad(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpu",
                kind=MetaData.Type.FLOAT,
                description="CPU %",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mem",
                kind=MetaData.Type.FLOAT,
                description="Memory % of total capacity",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pods",
                kind=MetaData.Type.FLOAT,
                description="Pods % of maximum",
                default=0.0,
            )
        )
        self.baseType = 'KubeNodeLoad'
        self.service_type = self.baseType
        self.allTypes = ['KubeNodeLoad']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

