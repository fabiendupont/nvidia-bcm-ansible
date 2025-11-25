from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.pbsprorole import PbsProRole


class PbsProClientRole(PbsProRole):
    """
    PbsPro client role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="slots",
                kind=MetaData.Type.STRING,
                description="Number of slots available on this node/category",
                default="AUTO",
            )
        )
        self.meta.add(
            MetaDataField(
                name="queues",
                kind=MetaData.Type.RESOLVE,
                description="Queues this node/nodes in this category belongs to",
                instance='PbsProJobQueue',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allQueues",
                kind=MetaData.Type.BOOL,
                description="When set, the role will provide all available queues. (The queues property will then be ignored.)",
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
                name="properties",
                kind=MetaData.Type.STRING,
                description="Node properties (a 'pnames' node attribute)",
                vector=True,
                default=[],
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
                name="momSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing pbs_mom daemon settings",
                instance='PbsProMomSettings',
                init_instance='PbsProMomSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="commSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing pbs_comm settings",
                instance='PbsProCommSettings',
                init_instance='PbsProCommSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeCustomizations",
                kind=MetaData.Type.ENTITY,
                description="PBS Pro node custom properties",
                instance='WlmNodeCustomizationEntry',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'PbsProClientRole'
        self.service_type = self.baseType
        self.allTypes = ['PbsProClientRole', 'PbsProRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

