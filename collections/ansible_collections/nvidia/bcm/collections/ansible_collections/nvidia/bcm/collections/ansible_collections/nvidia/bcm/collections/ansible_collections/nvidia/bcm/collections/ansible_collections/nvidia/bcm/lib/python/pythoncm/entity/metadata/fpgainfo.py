from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FPGAInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="vendor",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="bdf",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cardType",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="flashType",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dsaRunningFPGA",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dsaPackageInstalled",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="rev",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="serial",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="configMode",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fanPresence",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxPowerLevel",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac0",
                kind=MetaData.Type.STRING,
                function_check=MetaData.check_isMAC,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac1",
                kind=MetaData.Type.STRING,
                function_check=MetaData.check_isMAC,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac2",
                kind=MetaData.Type.STRING,
                function_check=MetaData.check_isMAC,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac3",
                kind=MetaData.Type.STRING,
                function_check=MetaData.check_isMAC,
                default='00:00:00:00:00:00',
            )
        )
        self.baseType = 'FPGAInfo'
        self.service_type = self.baseType
        self.allTypes = ['FPGAInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

