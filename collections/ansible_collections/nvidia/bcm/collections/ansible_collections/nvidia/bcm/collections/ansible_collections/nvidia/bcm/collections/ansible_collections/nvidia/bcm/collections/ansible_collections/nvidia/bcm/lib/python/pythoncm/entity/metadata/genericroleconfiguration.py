from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GenericRoleConfiguration(Entity):
    """
    Generic role configuration
    """
    class ServiceActionOnWrite(Enum):
        NONE = auto()
        RELOAD = auto()
        RESTART = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="createDirectory",
                kind=MetaData.Type.BOOL,
                description="Create directory if it doesn't exist",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="filename",
                kind=MetaData.Type.STRING,
                description="Filename",
                regex_check=r"^/.*$",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mask",
                kind=MetaData.Type.UINT,
                description="Filemask directory",
                default=0o644,
            )
        )
        self.meta.add(
            MetaDataField(
                name="userName",
                kind=MetaData.Type.STRING,
                description="User ownership applied to the file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupName",
                kind=MetaData.Type.STRING,
                description="Group ownership applied to the file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serviceActionOnWrite",
                kind=MetaData.Type.ENUM,
                description="Action performed on service if the file changed",
                options=[
                    self.ServiceActionOnWrite.NONE,
                    self.ServiceActionOnWrite.RELOAD,
                    self.ServiceActionOnWrite.RESTART,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ServiceActionOnWrite,
                default=self.ServiceActionOnWrite.RESTART,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serviceStopOnFailure",
                kind=MetaData.Type.BOOL,
                description="Stop services if the file write failed",
                default=True,
            )
        )
        self.baseType = 'GenericRoleConfiguration'
        self.service_type = self.baseType
        self.allTypes = ['GenericRoleConfiguration']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

