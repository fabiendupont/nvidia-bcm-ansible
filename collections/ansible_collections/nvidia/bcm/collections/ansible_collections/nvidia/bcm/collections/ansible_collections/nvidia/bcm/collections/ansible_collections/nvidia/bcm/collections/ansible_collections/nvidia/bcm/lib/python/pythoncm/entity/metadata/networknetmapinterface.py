from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkNetMapInterface(NetworkInterface):
    """
    Network NetMap interface
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=20,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkNetMapInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkNetMapInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

