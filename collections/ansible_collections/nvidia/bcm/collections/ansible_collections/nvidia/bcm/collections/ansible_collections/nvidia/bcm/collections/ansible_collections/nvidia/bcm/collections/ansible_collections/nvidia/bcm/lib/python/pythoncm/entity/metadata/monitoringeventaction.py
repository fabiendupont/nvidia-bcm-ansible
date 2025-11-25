from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringEventAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="profiles",
                kind=MetaData.Type.STRING,
                description="Inform all sessions with the specified profile, none is all",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="userNames",
                kind=MetaData.Type.STRING,
                description="Inform all sessions with the specified user names, none is all",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="mergeDelay",
                kind=MetaData.Type.FLOAT,
                description="Maximal action delay in order to merge with others",
                default=1.0,
            )
        )
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringEventAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringEventAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

