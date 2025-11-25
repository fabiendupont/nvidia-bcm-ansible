from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerdpusettingsevent import MonitoringDataProducerDPUSettingsEvent


class MonitoringDataProducerDPUSettingsEventTile(MonitoringDataProducerDPUSettingsEvent):
    class EventList(Enum):
        HNF_REQUESTS = auto()
        HNF_REJECTS = auto()
        ALL_BUSY = auto()
        MAF_BUSY = auto()
        MAF_REQUESTS = auto()
        RNF_REQUESTS = auto()
        REQUEST_TYPE = auto()
        MEMORY_READS = auto()
        MEMORY_WRITES = auto()
        VICTIM_WRITE = auto()
        POC_FULL = auto()
        POC_FAIL = auto()
        POC_SUCCESS = auto()
        POC_WRITES = auto()
        POC_READS = auto()
        FORWARD = auto()
        RXREQ_HNF = auto()
        RXRSP_HNF = auto()
        RXDAT_HNF = auto()
        TXREQ_HNF = auto()
        TXRSP_HNF = auto()
        TXDAT_HNF = auto()
        TXSNP_HNF = auto()
        INDEX_MATCH = auto()
        A72_ACCESS = auto()
        IO_ACCESS = auto()
        TSO_WRITE = auto()
        TSO_CONFLICT = auto()
        DIR_HIT = auto()
        HNF_ACCEPTS = auto()
        REQ_BUF_EMPTY = auto()
        REQ_BUF_IDLE_MAF = auto()
        TSO_NOARB = auto()
        TSO_NOARB_CYCLES = auto()
        MSS_NO_CREDIT = auto()
        TXDAT_NO_LCRD = auto()
        TXSNP_NO_LCRD = auto()
        TXRSP_NO_LCRD = auto()
        TXREQ_NO_LCRD = auto()
        TSO_CL_MATCH = auto()
        MEMORY_READS_BYPASS = auto()
        TSO_NOARB_TIMEOUT = auto()
        ALLOCATE = auto()
        VICTIM = auto()
        A72_WRITE = auto()
        A72_READ = auto()
        IO_WRITE = auto()
        IO_READ = auto()
        TSO_REJECT = auto()
        TXREQ_RN = auto()
        TXRSP_RN = auto()
        TXDAT_RN = auto()
        RXSNP_RN = auto()
        RXRSP_RN = auto()
        RXDAT_RN = auto()
        DISABLED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="event",
                kind=MetaData.Type.ENUM,
                description="Event value from the event list that will be sampled",
                options=[
                    self.EventList.HNF_REQUESTS,
                    self.EventList.HNF_REJECTS,
                    self.EventList.ALL_BUSY,
                    self.EventList.MAF_BUSY,
                    self.EventList.MAF_REQUESTS,
                    self.EventList.RNF_REQUESTS,
                    self.EventList.REQUEST_TYPE,
                    self.EventList.MEMORY_READS,
                    self.EventList.MEMORY_WRITES,
                    self.EventList.VICTIM_WRITE,
                    self.EventList.POC_FULL,
                    self.EventList.POC_FAIL,
                    self.EventList.POC_SUCCESS,
                    self.EventList.POC_WRITES,
                    self.EventList.POC_READS,
                    self.EventList.FORWARD,
                    self.EventList.RXREQ_HNF,
                    self.EventList.RXRSP_HNF,
                    self.EventList.RXDAT_HNF,
                    self.EventList.TXREQ_HNF,
                    self.EventList.TXRSP_HNF,
                    self.EventList.TXDAT_HNF,
                    self.EventList.TXSNP_HNF,
                    self.EventList.INDEX_MATCH,
                    self.EventList.A72_ACCESS,
                    self.EventList.IO_ACCESS,
                    self.EventList.TSO_WRITE,
                    self.EventList.TSO_CONFLICT,
                    self.EventList.DIR_HIT,
                    self.EventList.HNF_ACCEPTS,
                    self.EventList.REQ_BUF_EMPTY,
                    self.EventList.REQ_BUF_IDLE_MAF,
                    self.EventList.TSO_NOARB,
                    self.EventList.TSO_NOARB_CYCLES,
                    self.EventList.MSS_NO_CREDIT,
                    self.EventList.TXDAT_NO_LCRD,
                    self.EventList.TXSNP_NO_LCRD,
                    self.EventList.TXRSP_NO_LCRD,
                    self.EventList.TXREQ_NO_LCRD,
                    self.EventList.TSO_CL_MATCH,
                    self.EventList.MEMORY_READS_BYPASS,
                    self.EventList.TSO_NOARB_TIMEOUT,
                    self.EventList.ALLOCATE,
                    self.EventList.VICTIM,
                    self.EventList.A72_WRITE,
                    self.EventList.A72_READ,
                    self.EventList.IO_WRITE,
                    self.EventList.IO_READ,
                    self.EventList.TSO_REJECT,
                    self.EventList.TXREQ_RN,
                    self.EventList.TXRSP_RN,
                    self.EventList.TXDAT_RN,
                    self.EventList.RXSNP_RN,
                    self.EventList.RXRSP_RN,
                    self.EventList.RXDAT_RN,
                    self.EventList.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.EventList,
                default=self.EventList.DISABLED,
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettingsEvent'
        self.childType = 'MonitoringDataProducerDPUSettingsEventTile'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettingsEventTile', 'MonitoringDataProducerDPUSettingsEvent']
        self.top_level = False
        self.leaf_entity = True

