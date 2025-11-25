from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaletracker import ScaleTracker


class ScaleKubeNamespaceTracker(ScaleTracker):
    class TrackingScaleKubeObjects(Enum):
        job = auto()
        pod = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="controllerNamespace",
                kind=MetaData.Type.STRING,
                description="Tracking Kubernetes namespace name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="object",
                kind=MetaData.Type.ENUM,
                description="Type of Kubernetes objects to track",
                options=[
                    self.TrackingScaleKubeObjects.job,
                    self.TrackingScaleKubeObjects.pod,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.TrackingScaleKubeObjects,
                default=self.TrackingScaleKubeObjects.job,
            )
        )
        self.baseType = 'ScaleTracker'
        self.childType = 'ScaleKubeNamespaceTracker'
        self.service_type = self.baseType
        self.allTypes = ['ScaleKubeNamespaceTracker', 'ScaleTracker']
        self.top_level = False
        self.leaf_entity = True

