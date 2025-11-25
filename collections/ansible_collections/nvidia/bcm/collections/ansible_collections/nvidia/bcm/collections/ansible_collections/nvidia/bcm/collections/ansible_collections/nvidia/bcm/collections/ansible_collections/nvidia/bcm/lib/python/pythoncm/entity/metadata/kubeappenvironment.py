from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeAppEnvironment(Entity):
    """
    Kubernetes environment variables from applications
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                regex_check=r"^[a-zA-Z0-9_]+$",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="Value",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesEnvironment",
                kind=MetaData.Type.BOOL,
                description="Add variable to the nodes environment",
                default=False,
            )
        )
        self.baseType = 'KubeAppEnvironment'
        self.service_type = self.baseType
        self.allTypes = ['KubeAppEnvironment']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

