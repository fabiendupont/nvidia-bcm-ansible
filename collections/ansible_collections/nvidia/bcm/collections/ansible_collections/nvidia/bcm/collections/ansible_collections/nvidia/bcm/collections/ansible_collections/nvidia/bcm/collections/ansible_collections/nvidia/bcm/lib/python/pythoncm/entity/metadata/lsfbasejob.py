from pythoncm.entity.metadata.job import Job


class LSFBaseJob(Job):
    def __init__(self):
        super().__init__()
        self.baseType = 'Job'
        self.childType = 'LSFBaseJob'
        self.service_type = self.baseType
        self.allTypes = ['LSFBaseJob', 'Job']
        self.leaf_entity = False

