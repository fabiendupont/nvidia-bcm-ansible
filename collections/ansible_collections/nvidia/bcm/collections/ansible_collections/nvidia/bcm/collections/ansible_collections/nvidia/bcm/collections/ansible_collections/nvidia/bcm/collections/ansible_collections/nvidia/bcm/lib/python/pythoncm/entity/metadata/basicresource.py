from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BasicResource(Entity):
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
                name="dependency",
                kind=MetaData.Type.UUID,
                description="Dependency on another resource, run this resource on the same node as the dependency",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="exclude",
                kind=MetaData.Type.UUID,
                description="Do not run this resource on any node running one of the excluded resources",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable the resource from being given to any node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stopOnRemove",
                kind=MetaData.Type.BOOL,
                description="Automatically stop resource when removed",
                default=True,
            )
        )
        self.baseType = 'BasicResource'
        self.service_type = self.baseType
        self.allTypes = ['BasicResource']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

