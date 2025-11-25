from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OSServiceConfig(Entity):
    """
    OS service config
    """
    class RunCondition(Enum):
        ALWAYS = auto()
        ACTIVE = auto()
        PASSIVE = auto()
        PREFERPASSIVE = auto()

    class Priority(Enum):
        LOW = auto()
        DEFAULT = auto()
        HIGH = auto()

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
                name="from",
                kind=MetaData.Type.STRING,
                description="Name of the entity that this service was created from",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="monitored",
                kind=MetaData.Type.BOOL,
                description="CMDaemon will periodically check if the service is running",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="autostart",
                kind=MetaData.Type.BOOL,
                description="CMDaemon will restart a failed service",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runIf",
                kind=MetaData.Type.ENUM,
                description="Only run this service in the specified state",
                options=[
                    self.RunCondition.ALWAYS,
                    self.RunCondition.ACTIVE,
                    self.RunCondition.PASSIVE,
                    self.RunCondition.PREFERPASSIVE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.RunCondition,
                default=self.RunCondition.ALWAYS,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managed",
                kind=MetaData.Type.BOOL,
                description="Manage config files from cmd (if any)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addFromRole",
                kind=MetaData.Type.BOOL,
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fromGenericRole",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                clone=False,
                internal=True,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_role_uuid",
                kind=MetaData.Type.UUID,
                clone=False,
                internal=True,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_extra_uuid",
                kind=MetaData.Type.UUID,
                clone=False,
                internal=True,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="internal",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serviceType",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sicknessCheckScript",
                kind=MetaData.Type.STRING,
                description="Script for sickness checking (no script means no sickness checks)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sicknessCheckScriptTimeout",
                kind=MetaData.Type.UINT,
                description="Timeout after which the script is killed",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sicknessCheckInterval",
                kind=MetaData.Type.UINT,
                description="Sickness checks interval (rounded up to 30s monitoring interval)",
                default=60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="scriptTimeout",
                kind=MetaData.Type.INT,
                description="Service operation timeout",
                default=-1,
            )
        )
        self.baseType = 'OSServiceConfig'
        self.service_type = self.baseType
        self.allTypes = ['OSServiceConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'
        self.add_to_cluster = False
        self.allow_commit = False

