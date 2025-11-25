from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class MQTTRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="caPath",
                kind=MetaData.Type.STRING,
                description="CA certificate path",
                default="/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/etc/cacert.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="privateKeyPath",
                kind=MetaData.Type.STRING,
                description="Certificate path",
                default="/cm/local/apps/cmd/cm-mqtt/etc/mqtt.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="certificatePath",
                kind=MetaData.Type.STRING,
                description="Private key path",
                default="/cm/local/apps/cmd/cm-mqtt/etc/mqtt.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="writeNamedPipePath",
                kind=MetaData.Type.STRING,
                description="Named pipe to which cmd writes data back to MQTT servers",
                default="/var/spool/cmd/mqtt.pipe",
            )
        )
        self.meta.add(
            MetaDataField(
                name="servers",
                kind=MetaData.Type.ENTITY,
                description="Servers",
                instance='MQTTServer',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'MQTTRole'
        self.service_type = self.baseType
        self.allTypes = ['MQTTRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

