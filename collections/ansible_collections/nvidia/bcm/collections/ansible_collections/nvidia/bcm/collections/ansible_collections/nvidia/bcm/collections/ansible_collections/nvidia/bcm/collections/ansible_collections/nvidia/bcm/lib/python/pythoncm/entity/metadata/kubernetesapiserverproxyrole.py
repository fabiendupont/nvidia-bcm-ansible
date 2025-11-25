from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.basenginxrole import BaseNginxRole


class KubernetesApiServerProxyRole(BaseNginxRole):
    """
    Kubernetes api server proxy service
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="kubeClusters",
                kind=MetaData.Type.RESOLVE,
                description="The Kubernetes cluster instances (pointers)",
                instance='KubeCluster',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'KubernetesApiServerProxyRole'
        self.service_type = self.baseType
        self.allTypes = ['KubernetesApiServerProxyRole', 'BaseNginxRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

