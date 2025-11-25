from pythoncm.entity.metadata.job import Job


class SlurmJob(Job):
    """
    Slurm job
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'Job'
        self.childType = 'SlurmJob'
        self.service_type = self.baseType
        self.allTypes = ['SlurmJob', 'Job']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

