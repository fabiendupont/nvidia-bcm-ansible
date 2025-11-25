from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class CoolingDistributionUnit(Device):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="Device model name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="racks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks cooled by this unit",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Device'
        self.childType = 'CoolingDistributionUnit'
        self.service_type = self.baseType
        self.allTypes = ['CoolingDistributionUnit', 'Device']
        self.top_level = True
        self.leaf_entity = True

