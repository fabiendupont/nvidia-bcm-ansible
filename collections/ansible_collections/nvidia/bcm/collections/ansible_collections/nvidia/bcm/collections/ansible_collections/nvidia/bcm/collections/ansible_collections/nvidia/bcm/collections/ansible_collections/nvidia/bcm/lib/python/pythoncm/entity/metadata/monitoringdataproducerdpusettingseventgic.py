from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerdpusettingsevent import MonitoringDataProducerDPUSettingsEvent


class MonitoringDataProducerDPUSettingsEventGic(MonitoringDataProducerDPUSettingsEvent):
    class EventList(Enum):
        AW_REQ = auto()
        AW_BEATS = auto()
        AW_TRANS = auto()
        AW_RESP = auto()
        AW_STL = auto()
        AW_LAT = auto()
        AW_REQ_TBU = auto()
        AR_REQ = auto()
        AR_BEATS = auto()
        AR_TRANS = auto()
        AR_STL = auto()
        AR_LAT = auto()
        AR_REQ_TBU = auto()
        TBU_MISS = auto()
        TX_DAT_AF = auto()
        RX_DAT_AF = auto()
        RETRYQ_CRED = auto()
        DISABLED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="event",
                kind=MetaData.Type.ENUM,
                description="Event value from the event list that will be sampled",
                options=[
                    self.EventList.AW_REQ,
                    self.EventList.AW_BEATS,
                    self.EventList.AW_TRANS,
                    self.EventList.AW_RESP,
                    self.EventList.AW_STL,
                    self.EventList.AW_LAT,
                    self.EventList.AW_REQ_TBU,
                    self.EventList.AR_REQ,
                    self.EventList.AR_BEATS,
                    self.EventList.AR_TRANS,
                    self.EventList.AR_STL,
                    self.EventList.AR_LAT,
                    self.EventList.AR_REQ_TBU,
                    self.EventList.TBU_MISS,
                    self.EventList.TX_DAT_AF,
                    self.EventList.RX_DAT_AF,
                    self.EventList.RETRYQ_CRED,
                    self.EventList.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.EventList,
                default=self.EventList.DISABLED,
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettingsEvent'
        self.childType = 'MonitoringDataProducerDPUSettingsEventGic'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettingsEventGic', 'MonitoringDataProducerDPUSettingsEvent']
        self.top_level = False
        self.leaf_entity = True

