from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FSPartAssociation(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.RESOLVE,
                description="Node this association is associated with.",
                instance='Node',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncPoint",
                kind=MetaData.Type.STRING,
                description="Directory the FSPart should be synchronized to on the target.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="prefix",
                kind=MetaData.Type.STRING,
                description="Optional prefix to the sync point",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fspart",
                kind=MetaData.Type.RESOLVE,
                description="FSPart this association is associated with.",
                instance='FSPart',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableInHA",
                kind=MetaData.Type.BOOL,
                description="Enable in HA",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="onSharedStorage",
                kind=MetaData.Type.BOOL,
                description="FSPart associations on shared storage can be used as provisioning source, but don't need to be kept up-to-date.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupDirectory",
                kind=MetaData.Type.STRING,
                description="Backup directory",
                default='',
            )
        )
        self.baseType = 'FSPartAssociation'
        self.service_type = self.baseType
        self.allTypes = ['FSPartAssociation']
        self.leaf_entity = False
        self.add_to_cluster = False
        self.allow_commit = False

