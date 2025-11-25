from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmCgroupsSettings(Entity):
    """
    Wlm cgroups settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="mountPoint",
                kind=MetaData.Type.STRING,
                description="Where cgroups is mounted",
                default="/sys/fs/cgroup",
            )
        )
        self.baseType = 'WlmCgroupsSettings'
        self.service_type = self.baseType
        self.allTypes = ['WlmCgroupsSettings']
        self.leaf_entity = False

