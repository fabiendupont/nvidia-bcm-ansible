from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaleengine import ScaleEngine


class ScaleKubeEngine(ScaleEngine):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="cluster",
                kind=MetaData.Type.RESOLVE,
                description="Kubernetes cluster which pods will be tracked",
                instance='KubeCluster',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuBusyThreshold",
                kind=MetaData.Type.FLOAT,
                description="CPU load % that defines if node is too busy for new pods",
                default=0.9,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryBusyThreshold",
                kind=MetaData.Type.FLOAT,
                description="Memory load % that defines if node is too busy for new pods",
                default=0.9,
            )
        )
        self.baseType = 'ScaleEngine'
        self.childType = 'ScaleKubeEngine'
        self.service_type = self.baseType
        self.allTypes = ['ScaleKubeEngine', 'ScaleEngine']
        self.top_level = False
        self.leaf_entity = True

