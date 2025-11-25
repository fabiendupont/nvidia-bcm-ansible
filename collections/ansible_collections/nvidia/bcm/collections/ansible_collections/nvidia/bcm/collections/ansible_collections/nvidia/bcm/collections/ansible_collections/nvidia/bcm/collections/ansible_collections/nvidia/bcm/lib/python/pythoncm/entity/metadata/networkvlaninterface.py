from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkVLANInterface(NetworkInterface):
    """
    Network VLAN interface
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="reorder_hdr",
                kind=MetaData.Type.BOOL,
                description="When set to true the VLAN device will move the ethernet header around to make it look exactly like a real ethernet device.",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=50,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkVLANInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkVLANInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

