from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerSingleLineScript(MonitoringDataProducer):
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
                name="typeClass",
                kind=MetaData.Type.STRING,
                description="Type class, slash(/) separated for levels",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.FLOAT,
                description="Script timeout",
                default=5.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Additional arguments to pass to the script",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="runInBash",
                kind=MetaData.Type.BOOL,
                description="Run the script in a bash session",
                default=False,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerSingleLineScript'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerSingleLineScript', 'MonitoringDataProducer']
        self.leaf_entity = False

