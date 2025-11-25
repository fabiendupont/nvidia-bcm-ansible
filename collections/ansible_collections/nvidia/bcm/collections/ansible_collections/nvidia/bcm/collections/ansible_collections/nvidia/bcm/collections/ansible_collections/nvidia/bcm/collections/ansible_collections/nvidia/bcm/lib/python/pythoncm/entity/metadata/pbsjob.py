from pythoncm.entity.metadata.job import Job


class PBSJob(Job):
    def __init__(self):
        super().__init__()
        self.baseType = 'Job'
        self.childType = 'PBSJob'
        self.service_type = self.baseType
        self.allTypes = ['PBSJob', 'Job']
        self.leaf_entity = False

