from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.fspartassociation import FSPartAssociation


class FSPartBasicAssociation(FSPartAssociation):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="isRoot",
                kind=MetaData.Type.BOOL,
                description="Indicates if this association is the root file system for the target. A node can only have one association where this is set.",
                default=False,
            )
        )
        self.baseType = 'FSPartAssociation'
        self.childType = 'FSPartBasicAssociation'
        self.service_type = self.baseType
        self.allTypes = ['FSPartBasicAssociation', 'FSPartAssociation']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

