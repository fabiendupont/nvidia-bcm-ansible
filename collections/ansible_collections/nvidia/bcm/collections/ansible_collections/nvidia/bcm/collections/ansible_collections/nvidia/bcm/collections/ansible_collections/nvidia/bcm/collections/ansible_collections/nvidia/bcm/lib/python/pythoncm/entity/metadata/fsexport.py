from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FSExport(Entity):
    """
    Filesystem export
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Normally the same as the path, useful when exporting a path twice",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="path",
                kind=MetaData.Type.STRING,
                description="Path to export",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.RESOLVE,
                description="Network the interface is connected to",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hosts",
                kind=MetaData.Type.STRING,
                description="Specify extra hosts-range allowed access to this export (space separated)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="automatic",
                kind=MetaData.Type.BOOL,
                description="The export was created automatically",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowWrite",
                kind=MetaData.Type.BOOL,
                description="Allow writing",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="async",
                kind=MetaData.Type.BOOL,
                description="Allow the NFS server to violate the NFS protocol and reply to requests before any changes made by that request have been committed to stable storage",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rootSquash",
                kind=MetaData.Type.BOOL,
                description="Map requests from uid/gid 0 to the anonymous uid/gid",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allSquash",
                kind=MetaData.Type.BOOL,
                description="Map all uids and gids to the anonymous user",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="anonUid",
                kind=MetaData.Type.UINT,
                description="Anonymous account user id number",
                default=65534,
            )
        )
        self.meta.add(
            MetaDataField(
                name="anonGid",
                kind=MetaData.Type.UINT,
                description="Anonymous account group id number",
                default=65534,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraOptions",
                kind=MetaData.Type.STRING,
                description="Extra options to be added to this export",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fsid",
                kind=MetaData.Type.UINT,
                description="Identification for exports used in failover setup. Make sure these are identical",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rdma",
                kind=MetaData.Type.BOOL,
                description="Enable NFS over RDMA",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable the export",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="checkTree",
                kind=MetaData.Type.BOOL,
                description="Check tree",
                default=False,
            )
        )
        self.baseType = 'FSExport'
        self.service_type = self.baseType
        self.allTypes = ['FSExport']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

