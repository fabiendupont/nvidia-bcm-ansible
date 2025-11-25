from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkBridgeInterface(NetworkInterface):
    """
    Network bridge interface
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="stp",
                kind=MetaData.Type.BOOL,
                description="Spanning Tree Protocol enabled.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="forward_delay",
                kind=MetaData.Type.UINT,
                description="Frame forward delay (in seconds)",
                default=15,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interfaces",
                kind=MetaData.Type.STRING,
                description="List of interfaces which should be bridged.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=80,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkBridgeInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkBridgeInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

