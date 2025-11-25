from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringScriptAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="script",
                kind=MetaData.Type.STRING,
                description="Script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Arguments",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Timeout",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeEnvironment",
                kind=MetaData.Type.BOOL,
                description="Pass the node environment to the script",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runInShell",
                kind=MetaData.Type.BOOL,
                description="Run in shell",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mergeDelay",
                kind=MetaData.Type.FLOAT,
                description="Maximal action delay in order to merge with others",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mergeTrigger",
                kind=MetaData.Type.BOOL,
                description="Merge action from multiple triggers into one",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mergeMeasurable",
                kind=MetaData.Type.BOOL,
                description="Merge action from multiple measurables into one",
                default=False,
            )
        )
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringScriptAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringScriptAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

