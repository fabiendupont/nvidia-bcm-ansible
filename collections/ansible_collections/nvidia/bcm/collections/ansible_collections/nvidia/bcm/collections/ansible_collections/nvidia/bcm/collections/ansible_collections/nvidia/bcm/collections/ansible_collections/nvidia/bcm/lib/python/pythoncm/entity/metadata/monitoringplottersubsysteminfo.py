from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringPlotterSubSystemInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="first",
                kind=MetaData.Type.UINT,
                description="First plot request",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="last",
                kind=MetaData.Type.UINT,
                description="Last plot request",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="count",
                kind=MetaData.Type.UINT,
                description="Number of plot requests",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="samples",
                kind=MetaData.Type.UINT,
                description="Number of data samples",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sources",
                kind=MetaData.Type.UINT,
                description="Number of sources",
                default=0,
            )
        )
        self.baseType = 'MonitoringPlotterSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringPlotterSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

