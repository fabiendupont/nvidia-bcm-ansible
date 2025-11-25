from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.fspartassociation import FSPartAssociation


class FSPartProviderAssociation(FSPartAssociation):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="onlyWhenActive",
                kind=MetaData.Type.BOOL,
                description="Only use provider association if the node is the active head node",
                default=False,
            )
        )
        self.baseType = 'FSPartAssociation'
        self.childType = 'FSPartProviderAssociation'
        self.service_type = self.baseType
        self.allTypes = ['FSPartProviderAssociation', 'FSPartAssociation']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

