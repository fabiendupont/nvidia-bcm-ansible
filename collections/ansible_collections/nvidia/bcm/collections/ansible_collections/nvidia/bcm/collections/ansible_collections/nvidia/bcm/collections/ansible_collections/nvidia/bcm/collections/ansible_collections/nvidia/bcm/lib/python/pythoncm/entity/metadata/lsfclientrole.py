from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.lsfrole import LSFRole


class LSFClientRole(LSFRole):
    """
    LSF client role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="slots",
                kind=MetaData.Type.STRING,
                description="Number of slots available on this node/category",
                regex_check=r"^(auto|\d{1,5})$",
                default="auto",
            )
        )
        self.meta.add(
            MetaDataField(
                name="queues",
                kind=MetaData.Type.RESOLVE,
                description="Queues this node/nodes in this category belongs to",
                instance='LSFJobQueue',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allQueues",
                kind=MetaData.Type.BOOL,
                description="When set, the role will provide all available queues (the queues property will then be ignored)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpus",
                kind=MetaData.Type.UINT,
                description="Number of gpus",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuDevices",
                kind=MetaData.Type.STRING,
                description="/dev/* available to workload management",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="server",
                kind=MetaData.Type.BOOL,
                description="Is LSF server (can run jobs)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="IMEX",
                kind=MetaData.Type.BOOL,
                description="Start IMEX daemon from prolog/epilog",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostModel",
                kind=MetaData.Type.STRING,
                description="Host model (possible values are defined in lsf.shared)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostType",
                kind=MetaData.Type.STRING,
                description="Host type (possible values are defined in lsf.shared)",
                default="LINUX",
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeCustomizations",
                kind=MetaData.Type.ENTITY,
                description="LSF node custom properties",
                instance='WlmNodeCustomizationEntry',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'LSFClientRole'
        self.service_type = self.baseType
        self.allTypes = ['LSFClientRole', 'LSFRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

