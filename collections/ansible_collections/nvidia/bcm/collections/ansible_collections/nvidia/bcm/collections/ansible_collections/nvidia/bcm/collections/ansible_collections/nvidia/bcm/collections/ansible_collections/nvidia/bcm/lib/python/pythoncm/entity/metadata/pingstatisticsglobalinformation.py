from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PingStatisticsGlobalInformation(Entity):
    def __init__(self):
        super().__init__()
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
        self.baseType = 'PingStatisticsGlobalInformation'
        self.service_type = self.baseType
        self.allTypes = ['PingStatisticsGlobalInformation']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

