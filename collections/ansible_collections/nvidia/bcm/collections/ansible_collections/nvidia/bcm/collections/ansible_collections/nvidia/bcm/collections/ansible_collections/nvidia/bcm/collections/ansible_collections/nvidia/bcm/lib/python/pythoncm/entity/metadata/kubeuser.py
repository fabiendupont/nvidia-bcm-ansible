from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeUser(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="userName",
                kind=MetaData.Type.STRING,
                description="User name (not user ID)",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="manageKubeConfig",
                kind=MetaData.Type.BOOL,
                description="Write a kubeconfig file for this user",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="initialDefaultNamespace",
                kind=MetaData.Type.STRING,
                description="namespace to make default when creating kubeconfig",
                default='',
            )
        )
        self.baseType = 'KubeUser'
        self.service_type = self.baseType
        self.allTypes = ['KubeUser']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'userName'

