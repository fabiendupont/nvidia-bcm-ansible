from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BurnTestStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Test name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Test status",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="started",
                kind=MetaData.Type.BOOL,
                description="Indicates if test was started",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="passed",
                kind=MetaData.Type.BOOL,
                description="Indicates if test has passed",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failed",
                kind=MetaData.Type.BOOL,
                description="Indicates if test has failed",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="warning",
                kind=MetaData.Type.BOOL,
                description="Indicates if test produced a warning",
                default=False,
            )
        )
        self.baseType = 'BurnTestStatus'
        self.service_type = self.baseType
        self.allTypes = ['BurnTestStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

