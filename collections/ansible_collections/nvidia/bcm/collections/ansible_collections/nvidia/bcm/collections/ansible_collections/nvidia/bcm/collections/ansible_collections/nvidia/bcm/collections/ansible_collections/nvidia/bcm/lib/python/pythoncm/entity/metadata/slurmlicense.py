from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmLicense(Entity):
    """
    Slurm Licenses
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="License name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="count",
                kind=MetaData.Type.UINT,
                description="License number",
                default=0,
            )
        )
        self.baseType = 'SlurmLicense'
        self.service_type = self.baseType
        self.allTypes = ['SlurmLicense']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

