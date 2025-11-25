from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkTunnelInterface(NetworkInterface):
    """
    Network tunnel interface
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=30,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkTunnelInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkTunnelInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

