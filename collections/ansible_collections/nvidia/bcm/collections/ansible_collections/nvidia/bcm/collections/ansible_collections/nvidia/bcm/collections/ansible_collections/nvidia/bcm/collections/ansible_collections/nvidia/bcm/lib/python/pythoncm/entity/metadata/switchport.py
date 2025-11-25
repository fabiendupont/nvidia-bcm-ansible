from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SwitchPort(Entity):
    """
    Switch port
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="networkSwitch",
                kind=MetaData.Type.RESOLVE,
                description="Switch",
                instance='Switch',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port number on the switch",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="breakout",
                kind=MetaData.Type.INT,
                description="Breakout port number on the switch",
                default=-1,
            )
        )
        self.baseType = 'SwitchPort'
        self.service_type = self.baseType
        self.allTypes = ['SwitchPort']
        self.top_level = False
        self.leaf_entity = True

