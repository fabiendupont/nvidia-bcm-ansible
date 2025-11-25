from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringEmailAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="recipients",
                kind=MetaData.Type.STRING,
                description="Recipients",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allAdministrators",
                kind=MetaData.Type.BOOL,
                description="Also send e-mail to all administrator",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="server",
                kind=MetaData.Type.STRING,
                description="The SNMP server",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sender",
                kind=MetaData.Type.STRING,
                description="The sender of the e-mail",
                function_check=MetaData.check_isEmail,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                description="Extra information passed in the e-mail",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Timeout",
                default=15,
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
        self.childType = 'MonitoringEmailAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringEmailAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

