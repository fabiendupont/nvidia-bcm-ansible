from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GCPDisk(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the disk",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size of the disk",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.STRING,
                description="Type of the disk. If not specified, the default is pd-standard.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisionedIOPS",
                kind=MetaData.Type.UINT,
                description="I/O operations per second that the disk can handle.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisionedThroughput",
                kind=MetaData.Type.UINT,
                description="Throughput (in MB/s) that the disk can handle.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="source",
                kind=MetaData.Type.STRING,
                description="Source image to use to create the disk. Specify the source in the following format: global/images/my-image.",
                default='',
            )
        )
        self.baseType = 'GCPDisk'
        self.service_type = self.baseType
        self.allTypes = ['GCPDisk']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

