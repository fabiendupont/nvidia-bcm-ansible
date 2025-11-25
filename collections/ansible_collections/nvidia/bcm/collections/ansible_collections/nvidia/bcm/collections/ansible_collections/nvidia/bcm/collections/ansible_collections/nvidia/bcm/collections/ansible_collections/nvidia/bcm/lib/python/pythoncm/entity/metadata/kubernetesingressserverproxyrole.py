from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.basenginxrole import BaseNginxRole


class KubernetesIngressServerProxyRole(BaseNginxRole):
    """
    Kubernetes ingress server proxy service
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="listenPort",
                kind=MetaData.Type.UINT,
                description="TCP port listening for incoming connections",
                default=443,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ingressPort",
                kind=MetaData.Type.UINT,
                description="Specify manually the Ingress controller port. (Use 0 to disable)",
                default=0,
            )
        )
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
        self.childType = 'KubernetesIngressServerProxyRole'
        self.service_type = self.baseType
        self.allTypes = ['KubernetesIngressServerProxyRole', 'BaseNginxRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

