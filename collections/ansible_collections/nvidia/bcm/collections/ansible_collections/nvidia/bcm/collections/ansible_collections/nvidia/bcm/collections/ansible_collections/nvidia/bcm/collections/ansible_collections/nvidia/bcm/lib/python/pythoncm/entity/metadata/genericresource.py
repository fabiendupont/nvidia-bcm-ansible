from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.basicresource import BasicResource


class GenericResource(BasicResource):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="activateScript",
                kind=MetaData.Type.STRING,
                description="Script to be executed when the resource is given to a node",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="deactivateScript",
                kind=MetaData.Type.STRING,
                description="Script to be executed when the resource is taken a way from a node",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="checkScript",
                kind=MetaData.Type.STRING,
                description="Script to be executed periodically to verify the resource is still running",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Arguments to pass to the script",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="scriptTimeout",
                kind=MetaData.Type.UINT,
                description="Script timeout",
                default=15,
            )
        )
        self.baseType = 'BasicResource'
        self.childType = 'GenericResource'
        self.service_type = self.baseType
        self.allTypes = ['GenericResource', 'BasicResource']
        self.top_level = False
        self.leaf_entity = True

