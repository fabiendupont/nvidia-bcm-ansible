from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ScaleTracker(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Tracker name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Tracker is currently enabled or disabled",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="assignCategory",
                kind=MetaData.Type.RESOLVE,
                description="Category that should be assigned to managed nodes",
                instance='Category',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="primaryOverlays",
                kind=MetaData.Type.RESOLVE,
                description="Configuration overlays that managed nodes are added to when they are required by workload",
                instance='ConfigurationOverlay',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowedResourceProviders",
                kind=MetaData.Type.STRING,
                description="Only the specified resource providers will be used for a workload of this tracker (if empty than all allowed)",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="queueLengthThreshold",
                kind=MetaData.Type.UINT,
                description="Number of pending workloads/jobs that triggers the nodes bursting",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ageThreshold",
                kind=MetaData.Type.UINT,
                description="Workload/job pending time threshold that triggers the nodes bursting for this workload (in seconds)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="workloadsPerNode",
                kind=MetaData.Type.UINT,
                description="Number of workloads that can be scheduled to the same node at the same time (0 means no limit)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional tracker related parameters",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScaleTracker'
        self.service_type = self.baseType
        self.allTypes = ['ScaleTracker']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

