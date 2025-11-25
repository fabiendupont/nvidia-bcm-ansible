from pythoncm.entity.metadata.scaleengine import ScaleEngine


class ScaleGenericEngine(ScaleEngine):
    def __init__(self):
        super().__init__()
        self.baseType = 'ScaleEngine'
        self.childType = 'ScaleGenericEngine'
        self.service_type = self.baseType
        self.allTypes = ['ScaleGenericEngine', 'ScaleEngine']
        self.top_level = False
        self.leaf_entity = True

