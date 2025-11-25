from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PDUPort(Entity):
    """
    Power distribution unit port
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="pdu",
                kind=MetaData.Type.RESOLVE,
                description="Pointer to a power distribution unit",
                instance='PowerDistributionUnit',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port number on the power distribution unit",
                default=0,
            )
        )
        self.baseType = 'PDUPort'
        self.service_type = self.baseType
        self.allTypes = ['PDUPort']
        self.top_level = False
        self.leaf_entity = True

