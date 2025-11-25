from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class StaticRoute(Entity):
    """
    Static route
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Generally a unique combination of gateway ip and netmaskbits",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ip",
                kind=MetaData.Type.STRING,
                description="Destination IP",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gateway",
                kind=MetaData.Type.STRING,
                description="Gateway IP address",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="netmaskBits",
                kind=MetaData.Type.UINT,
                description="Destination netmask bits",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="metric",
                kind=MetaData.Type.UINT,
                description="Network metric for gateway priority, lower is higher",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.RESOLVE,
                description="Destination network the interface is connected to",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="networkDeviceName",
                kind=MetaData.Type.STRING,
                description="Name of network device",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.baseType = 'StaticRoute'
        self.service_type = self.baseType
        self.allTypes = ['StaticRoute']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

