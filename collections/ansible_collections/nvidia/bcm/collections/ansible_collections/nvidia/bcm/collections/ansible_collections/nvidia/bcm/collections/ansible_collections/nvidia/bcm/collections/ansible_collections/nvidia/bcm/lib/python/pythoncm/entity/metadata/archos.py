from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.archosinfo import ArchOSInfo


class ArchOS(ArchOSInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="primaryImage",
                kind=MetaData.Type.RESOLVE,
                description="Image used to boot new nodes and keep /cm/shared up to date, empty if head node is to be used",
                instance='SoftwareImage',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shared",
                kind=MetaData.Type.RESOLVE,
                description="Shared directory",
                instance='FSPart',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="installer",
                kind=MetaData.Type.RESOLVE,
                description="Node installer",
                instance='FSPart',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Priority",
                default=0,
            )
        )
        self.baseType = 'ArchOSInfo'
        self.childType = 'ArchOS'
        self.service_type = self.baseType
        self.allTypes = ['ArchOS', 'ArchOSInfo']
        self.top_level = False
        self.leaf_entity = True

