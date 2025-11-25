from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FileContent(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="filename",
                kind=MetaData.Type.STRING,
                description="Filename",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="content",
                kind=MetaData.Type.STRING,
                description="Content",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Username",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="permissions",
                kind=MetaData.Type.INT,
                description="Permissions",
                default=-1,
            )
        )
        self.baseType = 'FileContent'
        self.service_type = self.baseType
        self.allTypes = ['FileContent']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

