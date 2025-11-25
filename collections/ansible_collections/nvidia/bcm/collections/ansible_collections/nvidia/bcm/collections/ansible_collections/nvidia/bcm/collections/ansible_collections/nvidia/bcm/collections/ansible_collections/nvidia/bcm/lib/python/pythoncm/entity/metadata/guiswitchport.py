from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiSwitchPort(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port",
                default=0,
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
                name="status",
                kind=MetaData.Type.STRING,
                description="Status",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="uplink",
                kind=MetaData.Type.BOOL,
                description="Uplink",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_assigned_uuids",
                kind=MetaData.Type.UUID,
                description="The devices assigned to this port",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_detected_uuids",
                kind=MetaData.Type.UUID,
                description="The devices detected to this port via MAC",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="detected",
                kind=MetaData.Type.STRING,
                description="MAC addresses detected on this port",
                function_check=MetaData.check_isMAC,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="guid",
                kind=MetaData.Type.STRING,
                description="GUID detected on this port",
                default='',
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
                name="transmitted",
                kind=MetaData.Type.UINT,
                description="Transmitted",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="received",
                kind=MetaData.Type.UINT,
                description="Received",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="errors",
                kind=MetaData.Type.UINT,
                description="Errors",
                default=0,
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
        self.baseType = 'GuiSwitchPort'
        self.service_type = self.baseType
        self.allTypes = ['GuiSwitchPort']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

