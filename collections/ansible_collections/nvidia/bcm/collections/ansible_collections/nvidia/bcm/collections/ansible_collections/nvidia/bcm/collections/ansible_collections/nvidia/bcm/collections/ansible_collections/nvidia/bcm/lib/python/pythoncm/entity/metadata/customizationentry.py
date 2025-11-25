from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CustomizationEntry(Entity):
    """
    Customization entry
    """
    class CustomizationEntryAction(Enum):
        SMART_ADD = auto()
        APPEND = auto()
        PREPEND = auto()
        REMOVE = auto()
        PRESERVE = auto()
        DEFAULT = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="key",
                kind=MetaData.Type.STRING,
                description="Name of the key",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="Value for the key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="action",
                kind=MetaData.Type.ENUM,
                description="Determines how entres are added",
                options=[
                    self.CustomizationEntryAction.SMART_ADD,
                    self.CustomizationEntryAction.APPEND,
                    self.CustomizationEntryAction.PREPEND,
                    self.CustomizationEntryAction.REMOVE,
                    self.CustomizationEntryAction.PRESERVE,
                    self.CustomizationEntryAction.DEFAULT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CustomizationEntryAction,
                default=self.CustomizationEntryAction.SMART_ADD,
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
                name="separator",
                kind=MetaData.Type.STRING,
                default="",
            )
        )
        self.baseType = 'CustomizationEntry'
        self.service_type = self.baseType
        self.allTypes = ['CustomizationEntry']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'key'

