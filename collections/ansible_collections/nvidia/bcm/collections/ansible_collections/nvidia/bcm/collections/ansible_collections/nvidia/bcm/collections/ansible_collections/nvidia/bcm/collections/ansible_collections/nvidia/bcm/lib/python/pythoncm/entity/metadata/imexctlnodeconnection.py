from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ImexCtlNodeConnection(Entity):
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
                name="index",
                kind=MetaData.Type.UINT,
                description="Index inside the IMEX group",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ip",
                kind=MetaData.Type.STRING,
                description="The IP used",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Status",
                default='',
            )
        )
        self.baseType = 'ImexCtlNodeConnection'
        self.service_type = self.baseType
        self.allTypes = ['ImexCtlNodeConnection']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

