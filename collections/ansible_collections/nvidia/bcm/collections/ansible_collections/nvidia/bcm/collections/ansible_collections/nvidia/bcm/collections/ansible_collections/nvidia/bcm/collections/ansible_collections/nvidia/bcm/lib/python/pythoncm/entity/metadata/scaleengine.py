from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ScaleEngine(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="HPC workload engine name",
                required=True,
                default="hpc",
            )
        )
        self.meta.add(
            MetaDataField(
                name="trackers",
                kind=MetaData.Type.ENTITY,
                description="Workload trackers",
                instance='ScaleTracker',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="workloadsPerNode",
                kind=MetaData.Type.UINT,
                description="Number of workloads that can be scheduled to the same node at the same time",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Workload engine priority",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ageFactor",
                kind=MetaData.Type.FLOAT,
                description="Fairsharing coefficient for workload age significance",
                default=1.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="engineFactor",
                kind=MetaData.Type.FLOAT,
                description="Fairsharing coefficient for engine priority significance",
                default=1.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="externalPriorityFactor",
                kind=MetaData.Type.FLOAT,
                description="Fairsharing coefficient for external priority significance",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxNodes",
                kind=MetaData.Type.UINT,
                description="Allowed running nodes limit",
                default=32,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Engine related notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional engine related parameters that will be passed to cm-scale daemon",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScaleEngine'
        self.service_type = self.baseType
        self.allTypes = ['ScaleEngine']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

