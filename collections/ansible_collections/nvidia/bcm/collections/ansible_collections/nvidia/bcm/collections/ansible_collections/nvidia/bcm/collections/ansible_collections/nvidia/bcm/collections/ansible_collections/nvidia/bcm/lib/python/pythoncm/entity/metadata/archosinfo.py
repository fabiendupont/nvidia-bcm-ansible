from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ArchOSInfo(Entity):
    class Arch(Enum):
        x86_64 = auto()
        aarch64 = auto()

    class OS(Enum):
        rhel7 = auto()
        rhel8 = auto()
        sles12 = auto()
        sles15 = auto()
        ubuntu1804 = auto()
        ubuntu2004 = auto()
        ubuntu2204 = auto()
        rhel9 = auto()
        ubuntu2404 = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="arch",
                kind=MetaData.Type.ENUM,
                description="Architecture",
                options=[
                    self.Arch.x86_64,
                    self.Arch.aarch64,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Arch,
                default=self.Arch.x86_64,
            )
        )
        self.meta.add(
            MetaDataField(
                name="os",
                kind=MetaData.Type.ENUM,
                description="Operating system",
                options=[
                    self.OS.rhel8,
                    self.OS.sles15,
                    self.OS.ubuntu2004,
                    self.OS.ubuntu2204,
                    self.OS.rhel9,
                    self.OS.ubuntu2404,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OS,
                default=self.OS.rhel9,
            )
        )
        self.baseType = 'ArchOSInfo'
        self.service_type = self.baseType
        self.allTypes = ['ArchOSInfo']
        self.leaf_entity = False

