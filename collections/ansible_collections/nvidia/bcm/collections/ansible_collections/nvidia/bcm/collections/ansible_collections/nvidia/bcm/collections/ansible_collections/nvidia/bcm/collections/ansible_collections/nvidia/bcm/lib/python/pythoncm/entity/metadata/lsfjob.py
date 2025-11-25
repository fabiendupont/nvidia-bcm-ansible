from pythoncm.entity.metadata.lsfbasejob import LSFBaseJob


class LSFJob(LSFBaseJob):
    """
    LSF job
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'Job'
        self.childType = 'LSFJob'
        self.service_type = self.baseType
        self.allTypes = ['LSFJob', 'LSFBaseJob', 'Job']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

