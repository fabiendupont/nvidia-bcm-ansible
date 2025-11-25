from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class EtcdHostRole(Role):
    class LogLevel(Enum):
        INFO = auto()
        DEBUG = auto()
        WARN = auto()
        ERROR = auto()
        PANIC = auto()
        FATAL = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="memberName",
                kind=MetaData.Type.STRING,
                description="Human-readable name for this member ($hostname will be replaced to the node hostname)",
                default="$hostname",
            )
        )
        self.meta.add(
            MetaDataField(
                name="spool",
                kind=MetaData.Type.STRING,
                description="Path to the data directory",
                default="/var/lib/etcd",
            )
        )
        self.meta.add(
            MetaDataField(
                name="listenClientUrls",
                kind=MetaData.Type.STRING,
                description="List of URLs to listen on for client traffic",
                vector=True,
                default=["https://0.0.0.0:2379"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="listenPeerUrls",
                kind=MetaData.Type.STRING,
                description="List of URLs to listen on for peer traffic",
                vector=True,
                default=["https://0.0.0.0:2380"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="advertiseClientUrls",
                kind=MetaData.Type.STRING,
                description="List of this member's client URLs to advertise to the public",
                vector=True,
                default=["https://$ip:2379"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="advertisePeerUrls",
                kind=MetaData.Type.STRING,
                description="List of this member's peer URLs to advertise to the rest of the cluster",
                vector=True,
                default=["https://$ip:2380"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="snapshotCount",
                kind=MetaData.Type.UINT,
                description="Number of committed transactions to trigger a snapshot to disk",
                default=100000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxSnapshots",
                kind=MetaData.Type.UINT,
                description="Maximum number of snapshot files to retain (0 is unlimited)",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="loglevel",
                kind=MetaData.Type.ENUM,
                description="Log level, only supports debug, info, warn, error, panic, or fatal.",
                options=[
                    self.LogLevel.INFO,
                    self.LogLevel.DEBUG,
                    self.LogLevel.WARN,
                    self.LogLevel.ERROR,
                    self.LogLevel.PANIC,
                    self.LogLevel.FATAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.LogLevel,
                default=self.LogLevel.INFO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional parameters for etcd daemon",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="etcdCluster",
                kind=MetaData.Type.RESOLVE,
                description="The Etcd cluster instance",
                instance='EtcdCluster',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memberCertificate",
                kind=MetaData.Type.STRING,
                description="Etcd member certificate, signed with CA specified in the Etcd Cluster. When set it will overrule the value from the EtcdCluster object.",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="memberCertificateKey",
                kind=MetaData.Type.STRING,
                description="Etcd member certificate key, signed with CA specified in the Etcd Cluster. When set it will overrule the value from the EtcdCluster object.",
                default="",
            )
        )
        self.baseType = 'Role'
        self.childType = 'EtcdHostRole'
        self.service_type = self.baseType
        self.allTypes = ['EtcdHostRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

