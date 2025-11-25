from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class VersionInfo(Entity):
    """
    Version info
    """
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
                name="cmVersion",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonVersion",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonBuildIndex",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonBuildHash",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="databaseVersion",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'VersionInfo'
        self.service_type = self.baseType
        self.allTypes = ['VersionInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

