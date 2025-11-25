from pythoncm.entity.metadata.pbsjobqueue import PBSJobQueue


class PbsProJobQueue(PBSJobQueue):
    """
    PBSPro job queue
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'JobQueue'
        self.childType = 'PbsProJobQueue'
        self.service_type = self.baseType
        self.allTypes = ['PbsProJobQueue', 'PBSJobQueue', 'JobQueue']
        self.top_level = True
        self.leaf_entity = True

