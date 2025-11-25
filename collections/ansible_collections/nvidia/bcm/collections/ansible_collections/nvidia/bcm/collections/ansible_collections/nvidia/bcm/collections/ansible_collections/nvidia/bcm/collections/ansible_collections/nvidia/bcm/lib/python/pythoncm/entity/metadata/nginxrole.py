from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.basenginxrole import BaseNginxRole


class NginxRole(BaseNginxRole):
    """
    NGINX service
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nginxReverseProxy",
                kind=MetaData.Type.ENTITY,
                description="Nginx Reverse Proxy Configuration",
                instance='NginxReverseProxy',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'NginxRole'
        self.service_type = self.baseType
        self.allTypes = ['NginxRole', 'BaseNginxRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

