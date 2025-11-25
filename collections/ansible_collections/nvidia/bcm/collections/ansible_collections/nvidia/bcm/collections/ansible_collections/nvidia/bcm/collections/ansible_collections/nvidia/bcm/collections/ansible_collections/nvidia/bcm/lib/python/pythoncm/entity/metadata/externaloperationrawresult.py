from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.externaloperationresult import ExternalOperationResult


class ExternalOperationRawResult(ExternalOperationResult):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="output",
                kind=MetaData.Type.STRING,
                description="Output",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="error",
                kind=MetaData.Type.STRING,
                description="Error",
                default='',
            )
        )
        self.baseType = 'ExternalOperationResult'
        self.childType = 'ExternalOperationRawResult'
        self.service_type = self.baseType
        self.allTypes = ['ExternalOperationRawResult', 'ExternalOperationResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

