from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class AccessSettings(Entity):
    """
    Access settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Username for ssh and/or REST API",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password for ssh and/or REST API",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="rest_port",
                kind=MetaData.Type.UINT,
                description="Rest port, set to 0 to disable all REST calls",
                default=8765,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateInZtp",
                kind=MetaData.Type.BOOL,
                description="Update the switch password during ztp",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateInNV",
                kind=MetaData.Type.BOOL,
                description="Update the switch password using nv commands",
                default=False,
            )
        )
        self.baseType = 'AccessSettings'
        self.service_type = self.baseType
        self.allTypes = ['AccessSettings']
        self.top_level = False
        self.leaf_entity = True

