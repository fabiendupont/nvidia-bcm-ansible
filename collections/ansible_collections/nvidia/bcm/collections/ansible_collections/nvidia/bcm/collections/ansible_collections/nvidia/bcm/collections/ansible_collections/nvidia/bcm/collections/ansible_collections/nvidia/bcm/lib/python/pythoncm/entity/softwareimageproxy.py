#
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#

from __future__ import annotations

from pythoncm.entity.entity import Entity


class SoftwareImageProxy(Entity):
    NO_REVISION = -1
    LAST_REVISION = 0

    @property
    def software_image(self):
        """
        Get the software image.
        """
        image = self.parentSoftwareImage
        if image is None:
            return None
        if self.revisionID <= self.NO_REVISION:
            return image
        if len(image.revisionHistory) == 0:
            return image
        if self.revisionID == self.LAST_REVISION:
            return image.revisionHistory[-1].image
        return next((it.image for it in image.revisionHistory if it.revisionID == self.revisionID), None)

    @software_image.setter
    def software_image(self, image):
        """
        Set the software image.
        """
        if isinstance(image, Entity):
            self._cluster = image._cluster
        else:
            image = self._cluster.get_by_name(image, 'SoftwareImage')
        if image is None:
            raise ValueError('Image not specified')
        if image.parentSoftwareImage is None:
            self.revisionID = self.NO_REVISION
            self.parentSoftwareImage = image
        else:
            self.revisionID = image.revisionID
            self.parentSoftwareImage = image.parentSoftwareImage

    def set_no_revision(self):
        """
        Switch to the parent version of an image.
        """
        self.revisionID = self.NO_REVISION

    def set_latest_revision(self):
        """
        Switch to the latest image revision.
        """
        self.revisionID = self.LAST_REVISION
