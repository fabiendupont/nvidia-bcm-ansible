from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class CapiRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="labels",
                kind=MetaData.Type.STRING,
                description="labels to attach to the ByoHost CR in the form labelname=labelVal for e.g. '--label site=apac --label cores=2'",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="metricsBindAddress",
                kind=MetaData.Type.STRING,
                description="metricsbindaddress is the TCP address that the controller should bind to for serving prometheus metrics. It can be set to '0' to disable the metrics serving (default ':8888')",
                default=":8888",
            )
        )
        self.meta.add(
            MetaDataField(
                name="level",
                kind=MetaData.Type.UINT,
                description="Number for the log level verbosity",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional parameters for byoh host agent",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeCluster",
                kind=MetaData.Type.RESOLVE,
                description="The Kubernetes cluster instance (pointer)",
                instance='KubeCluster',
                default=None,
            )
        )
        self.baseType = 'Role'
        self.childType = 'CapiRole'
        self.service_type = self.baseType
        self.allTypes = ['CapiRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

