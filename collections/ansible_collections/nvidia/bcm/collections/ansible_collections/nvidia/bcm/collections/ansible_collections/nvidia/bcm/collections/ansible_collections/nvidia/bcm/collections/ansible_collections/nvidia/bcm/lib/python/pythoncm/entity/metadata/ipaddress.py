from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class IPAddress(Entity):
    class State(Enum):
        DOWN = auto()
        UP = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
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
                name="ip",
                kind=MetaData.Type.STRING,
                description="IP",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="netmask",
                kind=MetaData.Type.STRING,
                description="Netmask",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac",
                kind=MetaData.Type.STRING,
                description="MAC",
                function_check=MetaData.check_isMAC,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.ENUM,
                description="State",
                options=[
                    self.State.DOWN,
                    self.State.UP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.State,
                default=self.State.DOWN,
            )
        )
        self.meta.add(
            MetaDataField(
                name="alternatives",
                kind=MetaData.Type.STRING,
                description="Alternatives",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="mtu",
                kind=MetaData.Type.UINT,
                description="MTU",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="speed",
                kind=MetaData.Type.UINT,
                description="Speed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="duplex",
                kind=MetaData.Type.STRING,
                description="Duplex",
                default='',
            )
        )
        self.baseType = 'IPAddress'
        self.service_type = self.baseType
        self.allTypes = ['IPAddress']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

