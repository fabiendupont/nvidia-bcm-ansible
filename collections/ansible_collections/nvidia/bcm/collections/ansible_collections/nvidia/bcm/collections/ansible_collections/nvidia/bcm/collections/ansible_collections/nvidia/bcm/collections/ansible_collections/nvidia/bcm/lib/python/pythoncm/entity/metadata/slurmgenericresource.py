from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmGenericResource(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="alias",
                kind=MetaData.Type.STRING,
                description="Unique alias name of the generic resource",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the generic resource in Slurm",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="count",
                kind=MetaData.Type.STRING,
                description="Number of resources of this type available on this node (a suffix K, M, G, T or P may be used to multiply the number by 1024, 1048576, etc. respectively)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cores",
                kind=MetaData.Type.STRING,
                description="Specify the first thread CPU index numbers for the specific cores which can use this resource (e.g. '0,1,2,3' or '0-3')",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.STRING,
                description="An arbitrary string identifying the type of device",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="file",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of the device files associated with a resource (simple regular expressions are supported)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="consumable",
                kind=MetaData.Type.BOOL,
                description="Multiple jobs can use the same generic resource",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addToGresConfig",
                kind=MetaData.Type.BOOL,
                description="Add the generic resource entity to gres.conf",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="Flags",
                kind=MetaData.Type.STRING,
                description="Optional flags that can be specified to change configured behavior of the GRES",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="Links",
                kind=MetaData.Type.INT,
                description="A list of numbers identifying the number of connections between this device and other devices to allow coscheduling of better connected devices",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="MultipleFiles",
                kind=MetaData.Type.STRING,
                description="A list of device file paths (in the range format) associated with the GRES",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'SlurmGenericResource'
        self.service_type = self.baseType
        self.allTypes = ['SlurmGenericResource']
        self.top_level = False
        self.leaf_entity = True

