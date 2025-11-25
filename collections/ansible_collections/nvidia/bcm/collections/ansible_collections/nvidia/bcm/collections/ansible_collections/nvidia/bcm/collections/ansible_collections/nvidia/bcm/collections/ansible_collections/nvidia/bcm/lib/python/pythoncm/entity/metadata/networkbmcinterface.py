from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkBmcInterface(NetworkInterface):
    """
    Network BMC interface
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="mac",
                kind=MetaData.Type.STRING,
                description="The interfaces MAC address",
                function_check=MetaData.check_isMAC,
                clone=False,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gateway",
                kind=MetaData.Type.STRING,
                description="Gateway IP address, usually the head node's IP on the BMC network.",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="vlanid",
                kind=MetaData.Type.UINT,
                description="VLAN ID setting for the BMC card. When set to 0, VLAN capabilities are disabled.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lanchannel",
                kind=MetaData.Type.UINT,
                description="LAN channel for BMC interface",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=10,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkBmcInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkBmcInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

