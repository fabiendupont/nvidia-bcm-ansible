from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.externaloperationresult import ExternalOperationResult


class ExternalOperationJSONResult(ExternalOperationResult):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="output",
                kind=MetaData.Type.JSON,
                description="Output",
                default=None,
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
        self.childType = 'ExternalOperationJSONResult'
        self.service_type = self.baseType
        self.allTypes = ['ExternalOperationJSONResult', 'ExternalOperationResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

