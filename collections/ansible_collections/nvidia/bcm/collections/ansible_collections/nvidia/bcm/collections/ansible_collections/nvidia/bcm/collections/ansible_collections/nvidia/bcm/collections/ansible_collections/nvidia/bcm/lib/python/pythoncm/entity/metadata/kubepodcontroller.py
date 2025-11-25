from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubePodController(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Kubernetes pod controller name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.STRING,
                description="Kubernetes pod controller type",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeNamespace",
                kind=MetaData.Type.STRING,
                description="Namespace name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="uid",
                kind=MetaData.Type.STRING,
                description="Pod controller unique ID in Kubernetes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Pod controller start time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Pod controller creation time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="resources",
                kind=MetaData.Type.STRING,
                description="List of requested (if pending) or allocated (if started) resources",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="labels",
                kind=MetaData.Type.STRING,
                description="List of lables assigned to the controller object",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Current pod controller status",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="reason",
                kind=MetaData.Type.STRING,
                description="Pod controller status reason",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Workload priority",
                default=0,
            )
        )
        self.baseType = 'KubePodController'
        self.service_type = self.baseType
        self.allTypes = ['KubePodController']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

