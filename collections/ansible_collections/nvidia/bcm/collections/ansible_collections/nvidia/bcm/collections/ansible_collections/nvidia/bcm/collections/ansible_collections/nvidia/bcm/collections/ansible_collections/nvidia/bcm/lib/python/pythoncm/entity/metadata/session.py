from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Session(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="eventCounter",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="queuedEventSize",
                kind=MetaData.Type.UINT,
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientType",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="acknowledgedKeepAlive",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
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
                name="remoteAddress",
                kind=MetaData.Type.STRING,
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="group",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="idletime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'Session'
        self.service_type = self.baseType
        self.allTypes = ['Session']
        self.top_level = True
        self.leaf_entity = True

