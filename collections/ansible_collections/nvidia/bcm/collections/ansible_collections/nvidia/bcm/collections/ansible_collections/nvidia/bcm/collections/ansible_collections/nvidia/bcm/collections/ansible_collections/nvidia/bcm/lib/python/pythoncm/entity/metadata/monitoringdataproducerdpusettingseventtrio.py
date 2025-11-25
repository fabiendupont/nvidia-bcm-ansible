from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerdpusettingsevent import MonitoringDataProducerDPUSettingsEvent


class MonitoringDataProducerDPUSettingsEventTrio(MonitoringDataProducerDPUSettingsEvent):
    class EventList(Enum):
        TPIO_DATA_BEAT = auto()
        TDMA_DATA_BEAT = auto()
        MAP_DATA_BEAT = auto()
        TXMSG_DATA_BEAT = auto()
        TPIO_DATA_PACKET = auto()
        TDMA_DATA_PACKET = auto()
        MAP_DATA_PACKET = auto()
        TXMSG_DATA_PACKET = auto()
        TDMA_RT_AF = auto()
        TDMA_PBUF_MAC_AF = auto()
        TRIO_MAP_WRQ_BUF_EMPTY = auto()
        TRIO_MAP_CPL_BUF_EMPTY = auto()
        TRIO_MAP_RDQ0_BUF_EMPTY = auto()
        TRIO_MAP_RDQ1_BUF_EMPTY = auto()
        TRIO_MAP_RDQ2_BUF_EMPTY = auto()
        TRIO_MAP_RDQ3_BUF_EMPTY = auto()
        TRIO_MAP_RDQ4_BUF_EMPTY = auto()
        TRIO_MAP_RDQ5_BUF_EMPTY = auto()
        TRIO_MAP_RDQ6_BUF_EMPTY = auto()
        TRIO_MAP_RDQ7_BUF_EMPTY = auto()
        TRIO_RING_TX_FLIT_CH0 = auto()
        TRIO_RING_TX_FLIT_CH1 = auto()
        TRIO_RING_TX_FLIT_CH2 = auto()
        TRIO_RING_TX_FLIT_CH3 = auto()
        TRIO_RING_TX_FLIT_CH4 = auto()
        TRIO_RING_RX_FLIT_CH0 = auto()
        TRIO_RING_RX_FLIT_CH1 = auto()
        TRIO_RING_RX_FLIT_CH2 = auto()
        TRIO_RING_RX_FLIT_CH3 = auto()
        DISABLED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="event",
                kind=MetaData.Type.ENUM,
                description="Event value from the event list that will be sampled",
                options=[
                    self.EventList.TPIO_DATA_BEAT,
                    self.EventList.TDMA_DATA_BEAT,
                    self.EventList.MAP_DATA_BEAT,
                    self.EventList.TXMSG_DATA_BEAT,
                    self.EventList.TPIO_DATA_PACKET,
                    self.EventList.TDMA_DATA_PACKET,
                    self.EventList.MAP_DATA_PACKET,
                    self.EventList.TXMSG_DATA_PACKET,
                    self.EventList.TDMA_RT_AF,
                    self.EventList.TDMA_PBUF_MAC_AF,
                    self.EventList.TRIO_MAP_WRQ_BUF_EMPTY,
                    self.EventList.TRIO_MAP_CPL_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ0_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ1_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ2_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ3_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ4_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ5_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ6_BUF_EMPTY,
                    self.EventList.TRIO_MAP_RDQ7_BUF_EMPTY,
                    self.EventList.TRIO_RING_TX_FLIT_CH0,
                    self.EventList.TRIO_RING_TX_FLIT_CH1,
                    self.EventList.TRIO_RING_TX_FLIT_CH2,
                    self.EventList.TRIO_RING_TX_FLIT_CH3,
                    self.EventList.TRIO_RING_TX_FLIT_CH4,
                    self.EventList.TRIO_RING_RX_FLIT_CH0,
                    self.EventList.TRIO_RING_RX_FLIT_CH1,
                    self.EventList.TRIO_RING_RX_FLIT_CH2,
                    self.EventList.TRIO_RING_RX_FLIT_CH3,
                    self.EventList.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.EventList,
                default=self.EventList.DISABLED,
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettingsEvent'
        self.childType = 'MonitoringDataProducerDPUSettingsEventTrio'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettingsEventTrio', 'MonitoringDataProducerDPUSettingsEvent']
        self.top_level = False
        self.leaf_entity = True

