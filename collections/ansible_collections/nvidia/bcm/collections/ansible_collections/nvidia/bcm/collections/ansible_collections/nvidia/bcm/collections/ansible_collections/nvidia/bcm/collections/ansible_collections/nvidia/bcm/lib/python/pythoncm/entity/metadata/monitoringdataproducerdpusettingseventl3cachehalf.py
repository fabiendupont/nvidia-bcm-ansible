from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerdpusettingsevent import MonitoringDataProducerDPUSettingsEvent


class MonitoringDataProducerDPUSettingsEventL3CacheHalf(MonitoringDataProducerDPUSettingsEvent):
    class EventList(Enum):
        DISABLED = auto()
        CYCLES = auto()
        TOTAL_RD_REQ_IN = auto()
        TOTAL_WR_REQ_IN = auto()
        TOTAL_WR_DBID_ACK = auto()
        TOTAL_WR_DATA_IN = auto()
        TOTAL_WR_COMP = auto()
        TOTAL_RD_DATA_OUT = auto()
        TOTAL_CDN_REQ_IN_BANK0 = auto()
        TOTAL_CDN_REQ_IN_BANK1 = auto()
        TOTAL_DDN_REQ_IN_BANK0 = auto()
        TOTAL_DDN_REQ_IN_BANK1 = auto()
        TOTAL_EMEM_RD_RES_IN_BANK0 = auto()
        TOTAL_EMEM_RD_RES_IN_BANK1 = auto()
        TOTAL_CACHE_RD_RES_IN_BANK0 = auto()
        TOTAL_CACHE_RD_RES_IN_BANK1 = auto()
        TOTAL_EMEM_RD_REQ_BANK0 = auto()
        TOTAL_EMEM_RD_REQ_BANK1 = auto()
        TOTAL_EMEM_WR_REQ_BANK0 = auto()
        TOTAL_EMEM_WR_REQ_BANK1 = auto()
        TOTAL_RD_REQ_OUT = auto()
        TOTAL_WR_REQ_OUT = auto()
        TOTAL_RD_RES_IN = auto()
        HITS_BANK0 = auto()
        HITS_BANK1 = auto()
        MISSES_BANK0 = auto()
        MISSES_BANK1 = auto()
        ALLOCATIONS_BANK0 = auto()
        ALLOCATIONS_BANK1 = auto()
        EVICTIONS_BANK0 = auto()
        EVICTIONS_BANK1 = auto()
        DBID_REJECT = auto()
        WRDB_REJECT_BANK0 = auto()
        WRDB_REJECT_BANK1 = auto()
        CMDQ_REJECT_BANK0 = auto()
        CMDQ_REJECT_BANK1 = auto()
        COB_REJECT_BANK0 = auto()
        COB_REJECT_BANK1 = auto()
        TRB_REJECT_BANK0 = auto()
        TRB_REJECT_BANK1 = auto()
        TAG_REJECT_BANK0 = auto()
        TAG_REJECT_BANK1 = auto()
        ANY_REJECT_BANK0 = auto()
        ANY_REJECT_BANK1 = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="event",
                kind=MetaData.Type.ENUM,
                description="Event value from the event list that will be sampled",
                options=[
                    self.EventList.DISABLED,
                    self.EventList.CYCLES,
                    self.EventList.TOTAL_RD_REQ_IN,
                    self.EventList.TOTAL_WR_REQ_IN,
                    self.EventList.TOTAL_WR_DBID_ACK,
                    self.EventList.TOTAL_WR_DATA_IN,
                    self.EventList.TOTAL_WR_COMP,
                    self.EventList.TOTAL_RD_DATA_OUT,
                    self.EventList.TOTAL_CDN_REQ_IN_BANK0,
                    self.EventList.TOTAL_CDN_REQ_IN_BANK1,
                    self.EventList.TOTAL_DDN_REQ_IN_BANK0,
                    self.EventList.TOTAL_DDN_REQ_IN_BANK1,
                    self.EventList.TOTAL_EMEM_RD_RES_IN_BANK0,
                    self.EventList.TOTAL_EMEM_RD_RES_IN_BANK1,
                    self.EventList.TOTAL_CACHE_RD_RES_IN_BANK0,
                    self.EventList.TOTAL_CACHE_RD_RES_IN_BANK1,
                    self.EventList.TOTAL_EMEM_RD_REQ_BANK0,
                    self.EventList.TOTAL_EMEM_RD_REQ_BANK1,
                    self.EventList.TOTAL_EMEM_WR_REQ_BANK0,
                    self.EventList.TOTAL_EMEM_WR_REQ_BANK1,
                    self.EventList.TOTAL_RD_REQ_OUT,
                    self.EventList.TOTAL_WR_REQ_OUT,
                    self.EventList.TOTAL_RD_RES_IN,
                    self.EventList.HITS_BANK0,
                    self.EventList.HITS_BANK1,
                    self.EventList.MISSES_BANK0,
                    self.EventList.MISSES_BANK1,
                    self.EventList.ALLOCATIONS_BANK0,
                    self.EventList.ALLOCATIONS_BANK1,
                    self.EventList.EVICTIONS_BANK0,
                    self.EventList.EVICTIONS_BANK1,
                    self.EventList.DBID_REJECT,
                    self.EventList.WRDB_REJECT_BANK0,
                    self.EventList.WRDB_REJECT_BANK1,
                    self.EventList.CMDQ_REJECT_BANK0,
                    self.EventList.CMDQ_REJECT_BANK1,
                    self.EventList.COB_REJECT_BANK0,
                    self.EventList.COB_REJECT_BANK1,
                    self.EventList.TRB_REJECT_BANK0,
                    self.EventList.TRB_REJECT_BANK1,
                    self.EventList.TAG_REJECT_BANK0,
                    self.EventList.TAG_REJECT_BANK1,
                    self.EventList.ANY_REJECT_BANK0,
                    self.EventList.ANY_REJECT_BANK1,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.EventList,
                default=self.EventList.DISABLED,
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettingsEvent'
        self.childType = 'MonitoringDataProducerDPUSettingsEventL3CacheHalf'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettingsEventL3CacheHalf', 'MonitoringDataProducerDPUSettingsEvent']
        self.top_level = False
        self.leaf_entity = True

