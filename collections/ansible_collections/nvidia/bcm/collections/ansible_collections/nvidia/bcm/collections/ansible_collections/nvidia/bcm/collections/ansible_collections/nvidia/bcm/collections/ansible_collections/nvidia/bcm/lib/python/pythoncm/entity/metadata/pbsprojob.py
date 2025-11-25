from pythoncm.entity.metadata.pbsjob import PBSJob


class PbsProJob(PBSJob):
    """
    PBSPro job
    """
    def __init__(self):
        super().__init__()
        self.baseType = 'Job'
        self.childType = 'PbsProJob'
        self.service_type = self.baseType
        self.allTypes = ['PbsProJob', 'PBSJob', 'Job']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

