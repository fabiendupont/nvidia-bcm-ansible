from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ClusterSetup(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_partition_uuid",
                kind=MetaData.Type.UUID,
                description="Partition",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="CMID",
                kind=MetaData.Type.UINT,
                description="CMID",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="databaseVersion",
                kind=MetaData.Type.UINT,
                description="Database version",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="organization",
                kind=MetaData.Type.STRING,
                description="Organization",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerOnDelay",
                kind=MetaData.Type.FLOAT,
                description="Delay in seconds between powering on nodes",
                regex_check=r"^\d{1,2}(\.\d)?$",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerOffDelay",
                kind=MetaData.Type.FLOAT,
                description="Delay in seconds between powering off nodes",
                regex_check=r"^\d{1,2}(\.\d)?$",
                default=1,
            )
        )
        self.baseType = 'ClusterSetup'
        self.service_type = self.baseType
        self.allTypes = ['ClusterSetup']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

