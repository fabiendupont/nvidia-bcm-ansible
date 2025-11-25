from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSCluster(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the BeeGFS cluster",
                regex_check=r"^[a-zA-Z0-9_]+$",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="multiMode",
                kind=MetaData.Type.BOOL,
                description="BeeGFS multi mode enabled",
                diff_type=MetaDataField.Diff.disabled,
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountpoint",
                kind=MetaData.Type.STRING,
                description="Path to a beegfs filesystem mountpoint",
                regex_check=r"^/[^\s\0]+$",
                diff_type=MetaDataField.Diff.disabled,
                default="/mnt/beegfs",
            )
        )
        self.meta.add(
            MetaDataField(
                name="authFile",
                kind=MetaData.Type.STRING,
                description="Path to the shared secret authentication file",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.baseType = 'BeeGFSCluster'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSCluster']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

