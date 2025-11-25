from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ConfigFileVersion(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="filename",
                kind=MetaData.Type.STRING,
                description="File name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="content",
                kind=MetaData.Type.STRING,
                description="Content of the file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Creation time",
                default=0,
            )
        )
        self.baseType = 'ConfigFileVersion'
        self.service_type = self.baseType
        self.allTypes = ['ConfigFileVersion']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

