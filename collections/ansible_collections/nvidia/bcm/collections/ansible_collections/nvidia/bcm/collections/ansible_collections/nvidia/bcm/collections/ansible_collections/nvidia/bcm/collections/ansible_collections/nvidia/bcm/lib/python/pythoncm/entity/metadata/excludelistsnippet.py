from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ExcludeListSnippet(Entity):
    """
    Exclude list snippet
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeList",
                kind=MetaData.Type.STRING,
                description="Excluded paths in the node image update",
                vector=True,
                default=[],
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
                name="noNewFiles",
                kind=MetaData.Type.BOOL,
                description="No new files",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="modeSync",
                kind=MetaData.Type.BOOL,
                description="Include this snippet when mode is sync",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="modeFull",
                kind=MetaData.Type.BOOL,
                description="Include this snippet when mode is full",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="modeUpdate",
                kind=MetaData.Type.BOOL,
                description="Include this snippet when mode is update",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="modeGrab",
                kind=MetaData.Type.BOOL,
                description="Include this snippet when mode is grab",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="modeGrabNew",
                kind=MetaData.Type.BOOL,
                description="Include this snippet when mode is grab new",
                default=False,
            )
        )
        self.baseType = 'ExcludeListSnippet'
        self.service_type = self.baseType
        self.allTypes = ['ExcludeListSnippet']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

