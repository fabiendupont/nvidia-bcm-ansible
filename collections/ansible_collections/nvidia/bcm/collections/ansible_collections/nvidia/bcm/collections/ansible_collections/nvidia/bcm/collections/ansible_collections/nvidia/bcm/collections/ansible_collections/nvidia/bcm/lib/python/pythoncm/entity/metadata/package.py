from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Package(Entity):
    class Type(Enum):
        UNDEFINED = auto()
        RPM = auto()
        DEB = auto()

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
                name="type",
                kind=MetaData.Type.ENUM,
                description="Type of package manager",
                options=[
                    self.Type.UNDEFINED,
                    self.Type.RPM,
                    self.Type.DEB,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="path",
                kind=MetaData.Type.STRING,
                description="Path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="release",
                kind=MetaData.Type.STRING,
                description="Release",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arch",
                kind=MetaData.Type.STRING,
                description="Architecture",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="buildDate",
                kind=MetaData.Type.TIMESTAMP,
                description="Build date",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="installDate",
                kind=MetaData.Type.TIMESTAMP,
                description="Install date",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="installed",
                kind=MetaData.Type.BOOL,
                description="Installed",
                default=False,
            )
        )
        self.baseType = 'Package'
        self.service_type = self.baseType
        self.allTypes = ['Package']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

