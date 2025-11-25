from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringServiceAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="service",
                kind=MetaData.Type.STRING,
                description="Service",
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
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringServiceAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringServiceAction', 'MonitoringAction']
        self.leaf_entity = False

