from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaleresourceprovider import ScaleResourceProvider


class ScaleDynamicNodesProvider(ScaleResourceProvider):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="templateNode",
                kind=MetaData.Type.RESOLVE,
                description="Template node",
                instance='Node',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeRange",
                kind=MetaData.Type.STRING,
                description="Node range",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="networkInterface",
                kind=MetaData.Type.STRING,
                description="Which node network interface will be changed on cloning (incremented)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTemplateNode",
                kind=MetaData.Type.BOOL,
                description="Should template node be started automatically",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stopTemplateNode",
                kind=MetaData.Type.BOOL,
                description="Should template node be stopped automatically",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="removeNodes",
                kind=MetaData.Type.BOOL,
                description="Should nodes be removed from Bright Cluster Manager configuration upon the node termination",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leaveFailedNodes",
                kind=MetaData.Type.BOOL,
                description="Failed nodes will not be touched in order to allow administrator to investigate why they were failed",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="neverTerminate",
                kind=MetaData.Type.UINT,
                description="Number of nodes that cm-scale powers off and allows to remain, instead of terminating",
                default=32,
            )
        )
        self.meta.add(
            MetaDataField(
                name="neverTerminateNodes",
                kind=MetaData.Type.RESOLVE,
                description="List of particular nodes that cm-scale powers off and allows to remain, instead of terminating",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScaleResourceProvider'
        self.childType = 'ScaleDynamicNodesProvider'
        self.service_type = self.baseType
        self.allTypes = ['ScaleDynamicNodesProvider', 'ScaleResourceProvider']
        self.top_level = False
        self.leaf_entity = True

