from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class KubeletRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="kubeCluster",
                kind=MetaData.Type.RESOLVE,
                description="The Kubernetes cluster instance (pointer)",
                instance='KubeCluster',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="controlPlane",
                kind=MetaData.Type.BOOL,
                description="Control plane node",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="worker",
                kind=MetaData.Type.BOOL,
                description="Worker node",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="containerRuntimeService",
                kind=MetaData.Type.STRING,
                description="The container runtime systemd service",
                default="docker.service",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxPods",
                kind=MetaData.Type.UINT,
                description="Number of Pods that can run on this node",
                default=110,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.JSON,
                description="Options to overrule flags for Kube components",
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="custom_yaml",
                kind=MetaData.Type.STRING,
                description="Custom YAML to apply to /var/lib/kubelet/config.yaml",
                default="",
            )
        )
        self.baseType = 'Role'
        self.childType = 'KubeletRole'
        self.service_type = self.baseType
        self.allTypes = ['KubeletRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

