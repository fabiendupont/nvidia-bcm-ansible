from pythoncm.entity.metadata.lsfbasejobqueuestat import LSFBaseJobQueueStat


class LSFJobQueueStat(LSFBaseJobQueueStat):
    def __init__(self):
        super().__init__()
        self.baseType = 'JobQueueStat'
        self.childType = 'LSFJobQueueStat'
        self.service_type = self.baseType
        self.allTypes = ['LSFJobQueueStat', 'LSFBaseJobQueueStat', 'JobQueueStat']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

