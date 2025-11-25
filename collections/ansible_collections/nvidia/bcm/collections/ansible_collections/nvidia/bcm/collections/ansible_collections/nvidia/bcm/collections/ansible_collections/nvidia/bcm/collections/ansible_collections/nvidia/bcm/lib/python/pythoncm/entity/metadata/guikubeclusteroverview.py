from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiKubeClusterOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_kube_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="KubeCluster",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Cluster Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Kubernetes Version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="numNodes",
                kind=MetaData.Type.UINT,
                description="Number of nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numNamespaces",
                kind=MetaData.Type.UINT,
                description="Number of namespaces",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numServices",
                kind=MetaData.Type.UINT,
                description="Number of services",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numRcs",
                kind=MetaData.Type.UINT,
                description="Number of replication controllers",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numPvs",
                kind=MetaData.Type.UINT,
                description="Number of persistent volumes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numPvcs",
                kind=MetaData.Type.UINT,
                description="Number of persistent volumes claims",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobs",
                kind=MetaData.Type.ENTITY,
                description="Jobs",
                instance='JobInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="pods",
                kind=MetaData.Type.ENTITY,
                description="Pods",
                instance='KubePodInfo',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'GuiKubeClusterOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiKubeClusterOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

