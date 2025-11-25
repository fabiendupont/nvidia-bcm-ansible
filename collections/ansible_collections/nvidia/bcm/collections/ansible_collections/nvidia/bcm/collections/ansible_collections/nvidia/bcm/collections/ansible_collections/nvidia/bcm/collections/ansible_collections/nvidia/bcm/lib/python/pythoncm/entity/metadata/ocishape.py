from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudtype import CloudType


class OCIShape(CloudType):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="maxVnics",
                kind=MetaData.Type.UINT,
                description="The maximum number of VNIC attachments available for this shape.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="networkPorts",
                kind=MetaData.Type.UINT,
                description="The number of physical network interface card (NIC) ports available for this shape.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rdmaPorts",
                kind=MetaData.Type.UINT,
                description="The number of networking ports available for the remote direct memory access (RDMA) network between nodes in a high performance computing (HPC) cluster network. If the shape does not support cluster networks, this value is 0.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isFlexible",
                kind=MetaData.Type.BOOL,
                description="Whether the shape supports creating flexible instances. A flexible shape is a shape that lets you customize the number of OCPUs and the amount of memory when launching or resizing your instance.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpusMin",
                kind=MetaData.Type.UINT,
                description="The maximum number of OCPUs.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpusMax",
                kind=MetaData.Type.UINT,
                description="The maximum number of OCPUs.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryMin",
                kind=MetaData.Type.UINT,
                description="The minimum amount of memory.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryMax",
                kind=MetaData.Type.UINT,
                description="The maximum amount of memory.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryMinPerCpu",
                kind=MetaData.Type.UINT,
                description="The minimum amount of memory per OCPU available for this shape.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryMaxPerCpu",
                kind=MetaData.Type.UINT,
                description="The maximum amount of memory per OCPU available for this shape.",
                default=0,
            )
        )
        self.baseType = 'CloudType'
        self.childType = 'OCIShape'
        self.service_type = self.baseType
        self.allTypes = ['OCIShape', 'CloudType']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

