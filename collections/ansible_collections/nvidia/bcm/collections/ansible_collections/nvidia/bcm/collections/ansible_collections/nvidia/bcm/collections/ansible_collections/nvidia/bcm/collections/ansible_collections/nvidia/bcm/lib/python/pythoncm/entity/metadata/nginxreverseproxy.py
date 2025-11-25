from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NginxReverseProxy(Entity):
    """
    NGINX reverse proxy configuration
    """
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
                name="address",
                kind=MetaData.Type.STRING,
                description="Destination Network Address",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.RESOLVE,
                description="Destination hostname(only for nodes)",
                instance='Node',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="destport",
                kind=MetaData.Type.UINT,
                description="Port",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="Description",
                default="",
            )
        )
        self.baseType = 'NginxReverseProxy'
        self.service_type = self.baseType
        self.allTypes = ['NginxReverseProxy']
        self.top_level = False
        self.leaf_entity = True

