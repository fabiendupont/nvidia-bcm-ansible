from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PingStatisticsPairInformation(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="source",
                kind=MetaData.Type.UUID,
                description="",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="destination",
                kind=MetaData.Type.UUID,
                description="",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="count",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="average",
                kind=MetaData.Type.FLOAT,
                description="",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimum",
                kind=MetaData.Type.FLOAT,
                description="",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximum",
                kind=MetaData.Type.FLOAT,
                description="",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="uniformity",
                kind=MetaData.Type.FLOAT,
                description="",
                default=0.0,
            )
        )
        self.baseType = 'PingStatisticsPairInformation'
        self.service_type = self.baseType
        self.allTypes = ['PingStatisticsPairInformation']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

