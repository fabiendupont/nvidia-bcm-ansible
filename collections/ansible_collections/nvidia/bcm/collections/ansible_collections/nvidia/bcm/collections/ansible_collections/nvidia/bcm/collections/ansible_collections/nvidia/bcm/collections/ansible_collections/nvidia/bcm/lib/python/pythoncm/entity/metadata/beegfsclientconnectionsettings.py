from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSClientConnectionSettings(Entity):
    """
    BeeGFS client connection settings entry
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="portUDP",
                kind=MetaData.Type.UINT,
                description="UDP port for the client daemon",
                default=8004,
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
                name="communicationRetry",
                kind=MetaData.Type.UINT,
                description="Time for retries in case of a network failure",
                default=600,
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
                name="maxConcurrentAttempts",
                kind=MetaData.Type.UINT,
                description="This may help in case  establishing new connections keeps failing and produces fallbacks",
                default=0,
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
                name="rdmaBuffersNumber",
                kind=MetaData.Type.UINT,
                description="Number of RDMA buffers",
                default=70,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rdmaBufferSize",
                kind=MetaData.Type.UINT,
                description="Maximum size of a buffer that will be sent over the network",
                default=8192,
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
        self.meta.add(
            MetaDataField(
                name="unmountRetries",
                kind=MetaData.Type.BOOL,
                description="If communication error occurs during unmount, the unsuccessful communications will be retried normally.",
                default=True,
            )
        )
        self.baseType = 'BeeGFSClientConnectionSettings'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSClientConnectionSettings']
        self.top_level = False
        self.leaf_entity = True

