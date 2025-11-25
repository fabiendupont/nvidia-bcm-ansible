from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class BootRole(Role):
    """
    Boot role
    """
    class Sync(Enum):
        AUTO = auto()
        ALL = auto()
        CUSTOM = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodegroups",
                kind=MetaData.Type.RESOLVE,
                description="List of node groups which can boot from this node",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories which can boot from this node",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="racks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks which can boot from this node",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="softwareImages",
                kind=MetaData.Type.RESOLVE,
                description="List of software images from which can be booted, leave empty for all images",
                instance='SoftwareImage',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowRamdiskCreation",
                kind=MetaData.Type.BOOL,
                description="Allow the node to create ramdisks by itself, instead of waiting for them to be rsynced from the headnode",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableAutomaticExports",
                kind=MetaData.Type.BOOL,
                description="Disable creation of automatic filesystem exports",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="imagesFromProvisioningRole",
                kind=MetaData.Type.BOOL,
                description="Only allow nodes to boot from images defined in the provisioning role",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncFSParts",
                kind=MetaData.Type.ENUM,
                description="Sync FSParts mode",
                options=[
                    self.Sync.AUTO,
                    self.Sync.ALL,
                    self.Sync.CUSTOM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Sync,
                default=self.Sync.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fsparts",
                kind=MetaData.Type.RESOLVE,
                description="FSParts",
                instance='FSPart',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'BootRole'
        self.service_type = self.baseType
        self.allTypes = ['BootRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

