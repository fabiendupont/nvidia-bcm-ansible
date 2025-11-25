from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NVFabricInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="domain",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="hardStop",
                kind=MetaData.Type.BOOL,
                description="Hard stopped by an administrator",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_rack_uuids",
                kind=MetaData.Type.UUID,
                description="Rack",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_switch_uuids",
                kind=MetaData.Type.UUID,
                description="Switch",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_active_switch_uuid",
                kind=MetaData.Type.UUID,
                description="Switch that is active in the domain",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_all_active_switch_uuids",
                kind=MetaData.Type.UUID,
                description="Switch",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NVFabricInfo'
        self.service_type = self.baseType
        self.allTypes = ['NVFabricInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

