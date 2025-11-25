from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SoftwareImageFileSelection(Entity):
    """
    Software image file selection
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
                name="patterns",
                kind=MetaData.Type.STRING,
                description="Patterns to be included",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="watch",
                kind=MetaData.Type.BOOL,
                description="Watch files with inotify",
                default=False,
            )
        )
        self.baseType = 'SoftwareImageFileSelection'
        self.service_type = self.baseType
        self.allTypes = ['SoftwareImageFileSelection']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

