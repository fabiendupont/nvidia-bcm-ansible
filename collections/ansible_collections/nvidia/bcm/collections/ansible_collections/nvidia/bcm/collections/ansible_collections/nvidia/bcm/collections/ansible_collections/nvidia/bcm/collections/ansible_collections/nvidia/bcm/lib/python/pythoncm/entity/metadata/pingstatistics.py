from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PingStatistics(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="totalOk",
                kind=MetaData.Type.UINT,
                description="Total number of pings that returned OK",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalError",
                kind=MetaData.Type.UINT,
                description="Total number of pings that returned error",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalFailed",
                kind=MetaData.Type.UINT,
                description="Total number of pings that returned failed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalTimeout",
                kind=MetaData.Type.UINT,
                description="Total number of pings that returned timeout",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalNoAddress",
                kind=MetaData.Type.UINT,
                description="Total number of pings had no address",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalUnreachable",
                kind=MetaData.Type.UINT,
                description="Total number of pings that returned unreachable",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="total",
                kind=MetaData.Type.UINT,
                description="Total number of pings done",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pairInformation",
                kind=MetaData.Type.ENTITY,
                description="Ping pair information statistics",
                instance='PingStatisticsPairInformation',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="sourceInformation",
                kind=MetaData.Type.ENTITY,
                description="Ping source information statistics",
                instance='PingStatisticsSourceInformation',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="globalInformation",
                kind=MetaData.Type.ENTITY,
                description="Ping global information statistics",
                instance='PingStatisticsGlobalInformation',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="results",
                kind=MetaData.Type.ENTITY,
                description="Raw ping results",
                instance='PingResult',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'PingStatistics'
        self.service_type = self.baseType
        self.allTypes = ['PingStatistics']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

