from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerProcMount(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="includeMedia",
                kind=MetaData.Type.BOOL,
                description="Include media mount points",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeRemote",
                kind=MetaData.Type.BOOL,
                description="Include remote mount points",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeDocker",
                kind=MetaData.Type.BOOL,
                description="Include docker mount points",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeMountPoints",
                kind=MetaData.Type.STRING,
                description="Exclude mount points",
                vector=True,
                default=["^/snap/core/.*",                           "^/var/cloud-jobs/.*",                           "^/run/docker/runtime-nvidia/moby/.*",                           "^/run/docker/runtime-runc/moby/.*",                           "^/run/containerd/runc/.*",                           "^/var/lib/kubelet/.*",                           "^/var/lib/rancher/.*",                           "^/cm/local/apps/kubernetes/var/.*",                           "^/sys/fs/.*",                           "^.*/resolv.conf$",                           "^/var/lib/containerd/tmpmounts/.*"],
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerProcMount'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerProcMount', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

