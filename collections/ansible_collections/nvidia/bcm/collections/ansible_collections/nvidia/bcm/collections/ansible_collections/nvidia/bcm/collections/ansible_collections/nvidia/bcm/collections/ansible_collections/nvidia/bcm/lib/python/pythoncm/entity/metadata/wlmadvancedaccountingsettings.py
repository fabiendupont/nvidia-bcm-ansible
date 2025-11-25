from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmAdvancedAccountingSettings(Entity):
    """
    Workload management advanced accounting settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="managedHierarchy",
                kind=MetaData.Type.STRING,
                description="Representation of account name as a list of organizational entities",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="separator",
                kind=MetaData.Type.STRING,
                description="Separator of organizational entities in the account names",
                default="_",
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobCommentLabels",
                kind=MetaData.Type.STRING,
                description="User can tag a job with a label (a key in JSON object format) that is parsed and monitored by BCM",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="extractAccountingInfo",
                kind=MetaData.Type.BOOL,
                description="Extract accounting information, set to false to keep inside account/comments fields",
                default=True,
            )
        )
        self.baseType = 'WlmAdvancedAccountingSettings'
        self.service_type = self.baseType
        self.allTypes = ['WlmAdvancedAccountingSettings']
        self.top_level = False
        self.leaf_entity = True

