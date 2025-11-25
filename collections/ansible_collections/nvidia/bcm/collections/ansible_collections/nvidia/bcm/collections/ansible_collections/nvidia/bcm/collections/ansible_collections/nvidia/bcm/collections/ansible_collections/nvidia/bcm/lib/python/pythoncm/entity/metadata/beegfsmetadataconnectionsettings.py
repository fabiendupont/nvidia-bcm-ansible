from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSMetadataConnectionSettings(Entity):
    """
    BeeGFS metadata connection settings entry
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="portTCP",
                kind=MetaData.Type.UINT,
                description="TCP port for the service",
                default=8005,
            )
        )
        self.meta.add(
            MetaDataField(
                name="portUDP",
                kind=MetaData.Type.UINT,
                description="UDP port for the service",
                default=8005,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backlogTCP",
                kind=MetaData.Type.UINT,
                description="TCP listen backlog",
                default=128,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxInternodeNumber",
                kind=MetaData.Type.UINT,
                description="Max number of simultaneous connections to the same node",
                default=12,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fallbackExpiration",
                kind=MetaData.Type.UINT,
                description="Time after which a connection to a fallback interface expires",
                default=900,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interfacesFile",
                kind=MetaData.Type.STRING,
                description="Path to the file with a list of interfaces for communication",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="interfacesList",
                kind=MetaData.Type.STRING,
                description="List of interfaces for communication",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="netFilterFile",
                kind=MetaData.Type.STRING,
                description="Path to a file with a list of allowed IP subnets",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="tcpOnlyFilterFile",
                kind=MetaData.Type.STRING,
                description="Path to a file with a list of no-RDMA IP ranges",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="useRDMA",
                kind=MetaData.Type.BOOL,
                description="Use RDMA",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rdmaTypeOfService",
                kind=MetaData.Type.UINT,
                description="RDMA type of service",
                default=0,
            )
        )
        self.baseType = 'BeeGFSMetadataConnectionSettings'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSMetadataConnectionSettings']
        self.top_level = False
        self.leaf_entity = True

