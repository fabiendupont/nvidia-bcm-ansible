from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EtcdCluster(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the Etcd cluster",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="heartBeatInterval",
                kind=MetaData.Type.UINT,
                description="Time (in milliseconds) of a heartbeat interval",
                default=100,
            )
        )
        self.meta.add(
            MetaDataField(
                name="electionTimeout",
                kind=MetaData.Type.UINT,
                description="Time (in milliseconds) for an election to timeout",
                default=1000,
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
                name="ca",
                kind=MetaData.Type.STRING,
                description="The Certificate Authority (CA) Certificate path for Etcd, used to generate certificates for Etcd.",
                default="/etc/kubernetes/pki/default/etcd/ca.crt",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cakey",
                kind=MetaData.Type.STRING,
                description="The Certificate Authority (CA) Key path for Etcd, used to generate certificates for Etcd.",
                default="/etc/kubernetes/pki/default/etcd/ca.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="memberCertificate",
                kind=MetaData.Type.STRING,
                description="The Certificate path to use for Etcd cluster members, signed with the Etcd CA.",
                default="/etc/kubernetes/pki/default/etcd-member.crt",
            )
        )
        self.meta.add(
            MetaDataField(
                name="memberCertificateKey",
                kind=MetaData.Type.STRING,
                description="The Key path to use for Etcd cluster members, signed with the Etcd CA.",
                default="/etc/kubernetes/pki/default/etcd-member.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientCertificate",
                kind=MetaData.Type.STRING,
                description="The Client Certificate used for Etcdctl for example.",
                default="/etc/kubernetes/pki/default/apiserver-etcd-client.crt",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientCertificateKey",
                kind=MetaData.Type.STRING,
                description="The Client Certificate Key used for Etcdctl for example.",
                default="/etc/kubernetes/pki/default/apiserver-etcd-client.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientCA",
                kind=MetaData.Type.STRING,
                description="The Certificate Authority (CA) used for client certificates. When set it is assumed client certificate and key will be generated and signed with this CA by another party. Etcd still expects the path to be correct for the Client Certificate and Key.",
                default="/etc/kubernetes/pki/default/etcd/ca.crt",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientTypeEtcd",
                kind=MetaData.Type.UINT,
                description="client type in the CLIENT_TYPE_ETCD range",
                readonly=True,
                default=0,
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
        self.baseType = 'EtcdCluster'
        self.service_type = self.baseType
        self.allTypes = ['EtcdCluster']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

