from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class LabeledEntity(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="introductionTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Introduction time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lastUsedTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Time entity was last used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="permanent",
                kind=MetaData.Type.BOOL,
                description="Do not allow automatic deletion",
                default=False,
            )
        )
        self.baseType = 'LabeledEntity'
        self.service_type = self.baseType
        self.allTypes = ['LabeledEntity']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

