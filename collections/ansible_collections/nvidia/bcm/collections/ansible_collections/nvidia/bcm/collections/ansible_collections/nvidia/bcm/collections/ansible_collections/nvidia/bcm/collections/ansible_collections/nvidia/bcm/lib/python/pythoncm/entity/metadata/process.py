from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Process(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pid",
                kind=MetaData.Type.INT,
                description="Process ID",
                required=True,
                readonly=True,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ppid",
                kind=MetaData.Type.INT,
                description="Parent PID",
                readonly=True,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="uid",
                kind=MetaData.Type.INT,
                description="Owner UID",
                readonly=True,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gid",
                kind=MetaData.Type.INT,
                description="Process' group ID",
                readonly=True,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.STRING,
                description="Process' state",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmd",
                kind=MetaData.Type.STRING,
                description="The command name",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Virtual memory size",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rss",
                kind=MetaData.Type.UINT,
                description="Resident memory size",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nbthreads",
                kind=MetaData.Type.UINT,
                description="Number of threads spawned",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nbfiledescs",
                kind=MetaData.Type.UINT,
                description="Number of held file descriptors",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cputime",
                kind=MetaData.Type.UINT,
                description="CPU time",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuuse",
                kind=MetaData.Type.FLOAT,
                description="CPU usage",
                readonly=True,
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Owner name",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupname",
                kind=MetaData.Type.STRING,
                description="Group name",
                readonly=True,
                default='',
            )
        )
        self.baseType = 'Process'
        self.service_type = self.baseType
        self.allTypes = ['Process']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'pid'
        self.add_to_cluster = False
        self.allow_commit = False

