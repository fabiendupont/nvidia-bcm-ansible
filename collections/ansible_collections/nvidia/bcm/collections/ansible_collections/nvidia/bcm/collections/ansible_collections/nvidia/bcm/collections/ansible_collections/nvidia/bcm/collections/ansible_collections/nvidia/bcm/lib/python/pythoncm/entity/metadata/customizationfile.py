from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CustomizationFile(Entity):
    """
    Customization file
    """
    class CustomizationFileType(Enum):
        ENV = auto()
        INI = auto()
        Generic = auto()

    class CustomizationFileManagedSection(Enum):
        BEGIN_OF_FILE = auto()
        END_OF_FILE = auto()
        FORCE_BEGIN_OF_FILE = auto()
        FORCE_END_OF_FILE = auto()
        ENTIRE_FILE = auto()
        NONE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="entries",
                kind=MetaData.Type.ENTITY,
                description="Config file customization entries",
                instance='CustomizationEntry',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="label",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="Determines file type",
                options=[
                    self.CustomizationFileType.ENV,
                    self.CustomizationFileType.INI,
                    self.CustomizationFileType.Generic,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CustomizationFileType,
                default=self.CustomizationFileType.Generic,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managedsection",
                kind=MetaData.Type.ENUM,
                description="Determines how cmdaemon should customize the file",
                options=[
                    self.CustomizationFileManagedSection.BEGIN_OF_FILE,
                    self.CustomizationFileManagedSection.END_OF_FILE,
                    self.CustomizationFileManagedSection.FORCE_BEGIN_OF_FILE,
                    self.CustomizationFileManagedSection.FORCE_END_OF_FILE,
                    self.CustomizationFileManagedSection.ENTIRE_FILE,
                    self.CustomizationFileManagedSection.NONE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CustomizationFileManagedSection,
                default=self.CustomizationFileManagedSection.ENTIRE_FILE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="formatting",
                kind=MetaData.Type.STRING,
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                default=True,
            )
        )
        self.baseType = 'CustomizationFile'
        self.service_type = self.baseType
        self.allTypes = ['CustomizationFile']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

