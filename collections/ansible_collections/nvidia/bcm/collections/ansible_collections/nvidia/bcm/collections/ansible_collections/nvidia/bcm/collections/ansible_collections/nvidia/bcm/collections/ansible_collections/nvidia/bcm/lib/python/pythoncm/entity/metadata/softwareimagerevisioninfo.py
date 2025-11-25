from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SoftwareImageRevisionInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="image",
                kind=MetaData.Type.RESOLVE,
                clone=False,
                instance='SoftwareImage',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="revisionID",
                kind=MetaData.Type.INT,
                description="Revision ID",
                clone=False,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Revision creation time",
                readonly=True,
                clone=False,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="removalTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Revision removal time",
                readonly=True,
                clone=False,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="Revision Description",
                clone=False,
                default='',
            )
        )
        self.baseType = 'SoftwareImageRevisionInfo'
        self.service_type = self.baseType
        self.allTypes = ['SoftwareImageRevisionInfo']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

