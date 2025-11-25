from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FSPartInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_fspart_uuid",
                kind=MetaData.Type.UUID,
                description="FSPart",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="archOSInfo",
                kind=MetaData.Type.ENTITY,
                description="Detected arch/OS",
                instance='ArchOSInfo',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dgx",
                kind=MetaData.Type.BOOL,
                description="DGX image",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dgxVersion",
                kind=MetaData.Type.STRING,
                description="DGX image version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Total size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="inotifyWatcherSize",
                kind=MetaData.Type.UINT,
                description="Inotify watcher size",
                default=0,
            )
        )
        self.baseType = 'FSPartInfo'
        self.service_type = self.baseType
        self.allTypes = ['FSPartInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

