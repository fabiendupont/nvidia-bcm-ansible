from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DPUInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="index",
                kind=MetaData.Type.INT,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="opnStr",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.baseType = 'DPUInfo'
        self.service_type = self.baseType
        self.allTypes = ['DPUInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

