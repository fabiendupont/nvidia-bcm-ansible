from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GPUProfilingMetricInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpu",
                kind=MetaData.Type.UINT,
                description="GPU index",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="majorId",
                kind=MetaData.Type.UINT,
                description="Major ID",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minorId",
                kind=MetaData.Type.UINT,
                description="Minor ID",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fieldId",
                kind=MetaData.Type.UINT,
                description="Field ID",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="metric",
                kind=MetaData.Type.STRING,
                description="Metric",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Enabled",
                default=False,
            )
        )
        self.baseType = 'GPUProfilingMetricInfo'
        self.service_type = self.baseType
        self.allTypes = ['GPUProfilingMetricInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

