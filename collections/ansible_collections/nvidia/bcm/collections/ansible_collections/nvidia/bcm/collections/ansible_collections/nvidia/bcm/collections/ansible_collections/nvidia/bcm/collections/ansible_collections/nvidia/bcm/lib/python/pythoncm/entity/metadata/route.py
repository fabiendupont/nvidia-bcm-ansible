from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Route(Entity):
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
                name="destination",
                kind=MetaData.Type.STRING,
                description="The destination network or destination host.",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gateway",
                kind=MetaData.Type.STRING,
                description="Gateway",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="netmask",
                kind=MetaData.Type.STRING,
                description="The netmask for the destination",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="flags",
                kind=MetaData.Type.STRING,
                description="Flags",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="metric",
                kind=MetaData.Type.UINT,
                description="The 'distance' to the target (usually counted in hops)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref",
                kind=MetaData.Type.UINT,
                description="Number of references to this route",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="use",
                kind=MetaData.Type.UINT,
                description="Number of lookups for the route",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interface",
                kind=MetaData.Type.STRING,
                description="",
                default='',
            )
        )
        self.baseType = 'Route'
        self.service_type = self.baseType
        self.allTypes = ['Route']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

