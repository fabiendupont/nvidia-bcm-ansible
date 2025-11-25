from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaleengine import ScaleEngine


class ScaleHpcEngine(ScaleEngine):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="wlmCluster",
                kind=MetaData.Type.RESOLVE,
                description="WLM cluster that will be used by cm-scale",
                instance='WlmCluster',
                default=None,
            )
        )
        self.baseType = 'ScaleEngine'
        self.childType = 'ScaleHpcEngine'
        self.service_type = self.baseType
        self.allTypes = ['ScaleHpcEngine', 'ScaleEngine']
        self.top_level = False
        self.leaf_entity = True

