from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerdpusettingsevent import MonitoringDataProducerDPUSettingsEvent


class MonitoringDataProducerDPUSettingsEventTilenet(MonitoringDataProducerDPUSettingsEvent):
    class EventList(Enum):
        CDN_REQ = auto()
        DDN_REQ = auto()
        NDN_REQ = auto()
        CDN_DIAG_N_OUT_OF_CRED = auto()
        CDN_DIAG_S_OUT_OF_CRED = auto()
        CDN_DIAG_E_OUT_OF_CRED = auto()
        CDN_DIAG_W_OUT_OF_CRED = auto()
        CDN_DIAG_C_OUT_OF_CRED = auto()
        CDN_DIAG_N_EGRESS = auto()
        CDN_DIAG_S_EGRESS = auto()
        CDN_DIAG_E_EGRESS = auto()
        CDN_DIAG_W_EGRESS = auto()
        CDN_DIAG_C_EGRESS = auto()
        CDN_DIAG_N_INGRESS = auto()
        CDN_DIAG_S_INGRESS = auto()
        CDN_DIAG_E_INGRESS = auto()
        CDN_DIAG_W_INGRESS = auto()
        CDN_DIAG_C_INGRESS = auto()
        CDN_DIAG_CORE_SENT = auto()
        DDN_DIAG_N_OUT_OF_CRED = auto()
        DDN_DIAG_S_OUT_OF_CRED = auto()
        DDN_DIAG_E_OUT_OF_CRED = auto()
        DDN_DIAG_W_OUT_OF_CRED = auto()
        DDN_DIAG_C_OUT_OF_CRED = auto()
        DDN_DIAG_N_EGRESS = auto()
        DDN_DIAG_S_EGRESS = auto()
        DDN_DIAG_E_EGRESS = auto()
        DDN_DIAG_W_EGRESS = auto()
        DDN_DIAG_C_EGRESS = auto()
        DDN_DIAG_N_INGRESS = auto()
        DDN_DIAG_S_INGRESS = auto()
        DDN_DIAG_E_INGRESS = auto()
        DDN_DIAG_W_INGRESS = auto()
        DDN_DIAG_C_INGRESS = auto()
        DDN_DIAG_CORE_SENT = auto()
        NDN_DIAG_N_OUT_OF_CRED = auto()
        NDN_DIAG_S_OUT_OF_CRED = auto()
        NDN_DIAG_E_OUT_OF_CRED = auto()
        NDN_DIAG_W_OUT_OF_CRED = auto()
        NDN_DIAG_C_OUT_OF_CRED = auto()
        NDN_DIAG_N_EGRESS = auto()
        NDN_DIAG_S_EGRESS = auto()
        NDN_DIAG_E_EGRESS = auto()
        NDN_DIAG_W_EGRESS = auto()
        NDN_DIAG_C_EGRESS = auto()
        NDN_DIAG_N_INGRESS = auto()
        NDN_DIAG_S_INGRESS = auto()
        NDN_DIAG_E_INGRESS = auto()
        NDN_DIAG_W_INGRESS = auto()
        NDN_DIAG_C_INGRESS = auto()
        NDN_DIAG_CORE_SENT = auto()
        DISABLED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="event",
                kind=MetaData.Type.ENUM,
                description="Event value from the event list that will be sampled",
                options=[
                    self.EventList.CDN_REQ,
                    self.EventList.DDN_REQ,
                    self.EventList.NDN_REQ,
                    self.EventList.CDN_DIAG_N_OUT_OF_CRED,
                    self.EventList.CDN_DIAG_S_OUT_OF_CRED,
                    self.EventList.CDN_DIAG_E_OUT_OF_CRED,
                    self.EventList.CDN_DIAG_W_OUT_OF_CRED,
                    self.EventList.CDN_DIAG_C_OUT_OF_CRED,
                    self.EventList.CDN_DIAG_N_EGRESS,
                    self.EventList.CDN_DIAG_S_EGRESS,
                    self.EventList.CDN_DIAG_E_EGRESS,
                    self.EventList.CDN_DIAG_W_EGRESS,
                    self.EventList.CDN_DIAG_C_EGRESS,
                    self.EventList.CDN_DIAG_N_INGRESS,
                    self.EventList.CDN_DIAG_S_INGRESS,
                    self.EventList.CDN_DIAG_E_INGRESS,
                    self.EventList.CDN_DIAG_W_INGRESS,
                    self.EventList.CDN_DIAG_C_INGRESS,
                    self.EventList.CDN_DIAG_CORE_SENT,
                    self.EventList.DDN_DIAG_N_OUT_OF_CRED,
                    self.EventList.DDN_DIAG_S_OUT_OF_CRED,
                    self.EventList.DDN_DIAG_E_OUT_OF_CRED,
                    self.EventList.DDN_DIAG_W_OUT_OF_CRED,
                    self.EventList.DDN_DIAG_C_OUT_OF_CRED,
                    self.EventList.DDN_DIAG_N_EGRESS,
                    self.EventList.DDN_DIAG_S_EGRESS,
                    self.EventList.DDN_DIAG_E_EGRESS,
                    self.EventList.DDN_DIAG_W_EGRESS,
                    self.EventList.DDN_DIAG_C_EGRESS,
                    self.EventList.DDN_DIAG_N_INGRESS,
                    self.EventList.DDN_DIAG_S_INGRESS,
                    self.EventList.DDN_DIAG_E_INGRESS,
                    self.EventList.DDN_DIAG_W_INGRESS,
                    self.EventList.DDN_DIAG_C_INGRESS,
                    self.EventList.DDN_DIAG_CORE_SENT,
                    self.EventList.NDN_DIAG_N_OUT_OF_CRED,
                    self.EventList.NDN_DIAG_S_OUT_OF_CRED,
                    self.EventList.NDN_DIAG_E_OUT_OF_CRED,
                    self.EventList.NDN_DIAG_W_OUT_OF_CRED,
                    self.EventList.NDN_DIAG_C_OUT_OF_CRED,
                    self.EventList.NDN_DIAG_N_EGRESS,
                    self.EventList.NDN_DIAG_S_EGRESS,
                    self.EventList.NDN_DIAG_E_EGRESS,
                    self.EventList.NDN_DIAG_W_EGRESS,
                    self.EventList.NDN_DIAG_C_EGRESS,
                    self.EventList.NDN_DIAG_N_INGRESS,
                    self.EventList.NDN_DIAG_S_INGRESS,
                    self.EventList.NDN_DIAG_E_INGRESS,
                    self.EventList.NDN_DIAG_W_INGRESS,
                    self.EventList.NDN_DIAG_C_INGRESS,
                    self.EventList.NDN_DIAG_CORE_SENT,
                    self.EventList.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.EventList,
                default=self.EventList.DISABLED,
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettingsEvent'
        self.childType = 'MonitoringDataProducerDPUSettingsEventTilenet'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettingsEventTilenet', 'MonitoringDataProducerDPUSettingsEvent']
        self.top_level = False
        self.leaf_entity = True

