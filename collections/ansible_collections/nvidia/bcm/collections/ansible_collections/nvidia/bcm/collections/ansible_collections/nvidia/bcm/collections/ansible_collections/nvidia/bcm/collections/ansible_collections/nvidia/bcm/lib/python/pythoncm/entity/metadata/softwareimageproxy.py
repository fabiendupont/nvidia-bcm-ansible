from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SoftwareImageProxy(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="parentSoftwareImage",
                kind=MetaData.Type.RESOLVE,
                description="Parent software image",
                instance='SoftwareImage',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="revisionID",
                kind=MetaData.Type.INT,
                description="Revision ID",
                default=-1,
            )
        )
        self.baseType = 'SoftwareImageProxy'
        self.service_type = self.baseType
        self.allTypes = ['SoftwareImageProxy']
        self.top_level = False
        self.leaf_entity = True

