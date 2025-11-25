from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SyncInfo(Entity):
    class Mode(Enum):
        FULL = auto()
        SYNC = auto()
        UPDATE = auto()
        GRAB = auto()
        GRABNEW = auto()

    class Type(Enum):
        NORMAL = auto()
        NO_NEW_FILES = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.RESOLVE,
                instance='Node',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioningNode",
                kind=MetaData.Type.RESOLVE,
                instance='Node',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fspart",
                kind=MetaData.Type.RESOLVE,
                instance='FSPart',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mode",
                kind=MetaData.Type.ENUM,
                options=[
                    self.Mode.FULL,
                    self.Mode.SYNC,
                    self.Mode.UPDATE,
                    self.Mode.GRAB,
                    self.Mode.GRABNEW,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Mode,
                default=self.Mode.FULL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                options=[
                    self.Type.NORMAL,
                    self.Type.NO_NEW_FILES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.NORMAL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dryRun",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="endTime",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="exitCode",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="signal",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfFiles",
                kind=MetaData.Type.UINT,
                description="The count of all 'files' (in the generic sense), which includes directories, symlinks, etc.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfTransferredFiles",
                kind=MetaData.Type.UINT,
                description="The count of normal files that were updated via rsync's delta-transfer algorithm, which does not include created dirs, symlinks, etc.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfCreatedFiles",
                kind=MetaData.Type.UINT,
                description="The count of normal files that were created.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfDeletedFiles",
                kind=MetaData.Type.UINT,
                description="The count of normal files that were deleted.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalFileSize",
                kind=MetaData.Type.UINT,
                description="The total sum of all file sizes in the transfer. This does not count any size for directories or special files, but does include the size of symlinks.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalTransferredFileSize",
                kind=MetaData.Type.UINT,
                description="The total sum of all files sizes for just the transferred files.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="literalData",
                kind=MetaData.Type.UINT,
                description="How much unmatched file-update data we had to send to the receiver for it to recreate the updated files.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="matchedData",
                kind=MetaData.Type.UINT,
                description="How much data the receiver got locally when recreating the updated files.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileListSize",
                kind=MetaData.Type.UINT,
                description="How big the file-list data was when the sender sent it to the receiver. This is smaller than the in-memory size for the file list due to some compressing of duplicated data when rsync sends the list.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileListGenerationTime",
                kind=MetaData.Type.FLOAT,
                description="The number of seconds that the sender spent creating the file list. This requires a modern rsync on the sending side for this to be present.",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileListTransferTime",
                kind=MetaData.Type.FLOAT,
                description="The number of seconds that the sender spent sending the file list to the receiver.",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalSent",
                kind=MetaData.Type.UINT,
                description="The count of all the bytes that rsync sent from the client side to the server side.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalReceived",
                kind=MetaData.Type.UINT,
                description="The count of all non-message bytes that rsync received by the client side from the server side. 'Non-message' bytes means that we don't count the bytes for a verbose message that the server sent to us, which makes the stats more consistent.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="transferSpeed",
                kind=MetaData.Type.FLOAT,
                description="Transfer speed",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="speedup",
                kind=MetaData.Type.FLOAT,
                description="Speedup",
                default=0.0,
            )
        )
        self.baseType = 'SyncInfo'
        self.service_type = self.baseType
        self.allTypes = ['SyncInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

