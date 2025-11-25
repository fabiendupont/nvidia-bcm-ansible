from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkPhysicalInterface(NetworkInterface):
    """
    Network physical interface
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
                name="speed",
                kind=MetaData.Type.STRING,
                description="The interfaces network speed.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cardtype",
                kind=MetaData.Type.STRING,
                description="The type of network interface.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=60,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkPhysicalInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkPhysicalInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

