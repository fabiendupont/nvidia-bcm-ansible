from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class BaseNginxRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="workerConnections",
                kind=MetaData.Type.UINT,
                description="Number of worker connections",
                default=1024,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sendFile",
                kind=MetaData.Type.BOOL,
                description="Allow files to be sent",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tcpNoPush",
                kind=MetaData.Type.BOOL,
                description="",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tcpNoDelay",
                kind=MetaData.Type.BOOL,
                description="TCP no delay",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="keepAliveTimeout",
                kind=MetaData.Type.UINT,
                description="Keep alive timeout",
                default=65,
            )
        )
        self.meta.add(
            MetaDataField(
                name="typesHashMaxSize",
                kind=MetaData.Type.UINT,
                description="Types hash max size",
                default=2048,
            )
        )
        self.baseType = 'Role'
        self.childType = 'BaseNginxRole'
        self.service_type = self.baseType
        self.allTypes = ['BaseNginxRole', 'Role']
        self.leaf_entity = False

