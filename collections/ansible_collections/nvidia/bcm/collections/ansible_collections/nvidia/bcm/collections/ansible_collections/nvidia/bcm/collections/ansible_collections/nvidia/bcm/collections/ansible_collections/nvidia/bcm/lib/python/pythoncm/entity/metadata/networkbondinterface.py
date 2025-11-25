from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.networkinterface import NetworkInterface


class NetworkBondInterface(NetworkInterface):
    """
    Network bond interface
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
                name="mode",
                kind=MetaData.Type.INT,
                description="Bonding mode, see bonding.txt in the kernel documentation.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Options to pass to the bonding driver, see kernel documentation.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="interfaces",
                kind=MetaData.Type.STRING,
                description="List of interfaces which should be channel-bonded.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="onNetworkPriority",
                kind=MetaData.Type.UINT,
                description="Priority of DNS resolution queries for the interface on its network",
                default=70,
            )
        )
        self.baseType = 'NetworkInterface'
        self.childType = 'NetworkBondInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkBondInterface', 'NetworkInterface']
        self.top_level = False
        self.leaf_entity = True

