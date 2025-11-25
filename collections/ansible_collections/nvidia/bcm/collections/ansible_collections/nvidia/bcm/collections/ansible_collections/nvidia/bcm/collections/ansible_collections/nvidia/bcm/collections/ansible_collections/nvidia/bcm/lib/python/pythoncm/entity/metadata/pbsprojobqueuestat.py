from pythoncm.entity.metadata.pbsjobqueuestat import PBSJobQueueStat


class PbsProJobQueueStat(PBSJobQueueStat):
    def __init__(self):
        super().__init__()
        self.baseType = 'JobQueueStat'
        self.childType = 'PbsProJobQueueStat'
        self.service_type = self.baseType
        self.allTypes = ['PbsProJobQueueStat', 'PBSJobQueueStat', 'JobQueueStat']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

