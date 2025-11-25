from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NewNode(Entity):
    """
    New node
    """
    class Type(Enum):
        NODE = auto()
        DPUNODE = auto()
        SWITCH = auto()

    class Arch(Enum):
        UNDEFINED = auto()
        x86_64 = auto()
        aarch64 = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="switchPort",
                kind=MetaData.Type.ENTITY,
                description="Switch port the new node is connected to",
                instance='SwitchPort',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac",
                kind=MetaData.Type.STRING,
                description="MAC address of the new node",
                function_check=MetaData.check_isMAC,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ip",
                kind=MetaData.Type.STRING,
                description="IP address of the new node",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="Type of device",
                options=[
                    self.Type.NODE,
                    self.Type.DPUNODE,
                    self.Type.SWITCH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.NODE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="arch",
                kind=MetaData.Type.ENUM,
                description="Architecture",
                options=[
                    self.Arch.UNDEFINED,
                    self.Arch.x86_64,
                    self.Arch.aarch64,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Arch,
                default=self.Arch.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="firstSeen",
                kind=MetaData.Type.UINT,
                description="Uptime when the new node was first seen",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lastSeen",
                kind=MetaData.Type.UINT,
                description="Uptime when the new node was last seen",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="count",
                kind=MetaData.Type.UINT,
                description="Number of times the node was reported as new",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stop",
                kind=MetaData.Type.BOOL,
                description="Force the request to stop",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                description="Free text information string passed by node-installer",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="appeared",
                kind=MetaData.Type.TIMESTAMP,
                description="Timestamp when the new node first appeared",
                default=0,
            )
        )
        self.baseType = 'NewNode'
        self.service_type = self.baseType
        self.allTypes = ['NewNode']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

