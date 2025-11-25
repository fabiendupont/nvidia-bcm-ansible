from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeCluster(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the Kubernetes cluster",
                regex_check=r"^[^/\s\0]+$",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="etcdCluster",
                kind=MetaData.Type.RESOLVE,
                description="The Etcd cluster instance",
                instance='EtcdCluster',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serviceNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Network where service cluster IPs will be assigned from (must not overlap with any IP ranges assigned to nodes for pods)",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="podNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Network where POD IPs will be assigned from",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="podNetworkNodeMask",
                kind=MetaData.Type.STRING,
                description="Pod Network mask size for node cidr in cluster.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="internalNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Network to use to back the internal communications",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeDnsIp",
                kind=MetaData.Type.STRING,
                description="KubeDNS IP address",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubernetesApiServer",
                kind=MetaData.Type.STRING,
                description="Kubernetes API server address (format: https://host:port)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubernetesApiServerProxyPort",
                kind=MetaData.Type.UINT,
                description="Kubernetes API server proxy port",
                default=6444,
            )
        )
        self.meta.add(
            MetaDataField(
                name="appGroups",
                kind=MetaData.Type.ENTITY,
                description="Kubernetes applications managed by cmdaemon",
                instance='KubeAppGroup',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="labelSets",
                kind=MetaData.Type.ENTITY,
                description="Labels managed by cmdaemon",
                instance='KubeLabelSet',
                vector=True,
                default=[],
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
                name="version",
                kind=MetaData.Type.STRING,
                description="Kubernetes Cluster Version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="trustedDomains",
                kind=MetaData.Type.STRING,
                description="Trusted domains to be included in Kubernetes related certificates as Alt Subjects.",
                vector=True,
                default=["kubernetes", "kubernetes.default", "kubernetes.default.svc", "master", "localhost"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="moduleFileTemplate",
                kind=MetaData.Type.STRING,
                description="Template for system module file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeadm_init_file",
                kind=MetaData.Type.STRING,
                description="Kubeadm init file YAML",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeadm_init_cert_key",
                kind=MetaData.Type.STRING,
                description="Kubeadm CERT Key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeadm_ca_cert",
                kind=MetaData.Type.STRING,
                description="Kube CA Cert",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeadm_ca_key",
                kind=MetaData.Type.STRING,
                description="Kube CA Key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="users",
                kind=MetaData.Type.ENTITY,
                description="Kubernetes users",
                instance='KubeUser',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="external",
                kind=MetaData.Type.BOOL,
                description="External kubernetes cluster",
                diff_type=MetaDataField.Diff.disabled,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="externalIngressServer",
                kind=MetaData.Type.STRING,
                description="Kubernetes Ingress server address (format: https://host:port)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="externalPort",
                kind=MetaData.Type.UINT,
                description="External port, set to 0 to disable",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="capiTemplate",
                kind=MetaData.Type.BOOL,
                description="CAPI template kubernetes cluster",
                diff_type=MetaDataField.Diff.disabled,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="capiNamespace",
                kind=MetaData.Type.STRING,
                description="Kubernetes CAPI namespace",
                default="default",
            )
        )
        self.meta.add(
            MetaDataField(
                name="kubeCluster",
                kind=MetaData.Type.RESOLVE,
                description="The Kubernetes cluster instance managing this CAPI-deployed Kubernetes Cluster",
                instance='KubeCluster',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.JSON,
                description="Options to configure flags for Kube components",
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ingressProxyEnable",
                kind=MetaData.Type.BOOL,
                description="Ingress Proxy Enable Flag",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ingressProxyListenPort",
                kind=MetaData.Type.UINT,
                description="Ingress Proxy Listen Port",
                default=443,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ingressProxyBackendPort",
                kind=MetaData.Type.UINT,
                description="Ingress Proxy Backend Port, set to 0 to disable",
                default=0,
            )
        )
        self.baseType = 'KubeCluster'
        self.service_type = self.baseType
        self.allTypes = ['KubeCluster']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

