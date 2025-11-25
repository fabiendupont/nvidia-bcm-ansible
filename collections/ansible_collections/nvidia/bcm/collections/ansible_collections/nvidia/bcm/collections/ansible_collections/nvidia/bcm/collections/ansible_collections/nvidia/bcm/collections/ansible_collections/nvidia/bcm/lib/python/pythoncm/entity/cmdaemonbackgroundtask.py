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


class CMDaemonBackgroundTask(Entity):
    def completed(self) -> bool:
        """
        Check if the task has completed.
        """
        return self.status not in {
            self.meta.Status.PENDING,
            self.meta.Status.RUNNING,
        }

    def running(self) -> bool:
        """
        Check if the task has failed.
        """
        return self.status == self.meta.Status.RUNNING

    def pending(self) -> bool:
        """
        Check if the task has failed.
        """
        return self.status == self.meta.Status.PENDING

    def failed(self) -> bool:
        """
        Check if the task has failed.
        """
        return self.status == self.meta.Status.FAILED

    def success(self) -> bool:
        """
        Check if the task has finished successfully.
        """
        return self.status == self.meta.Status.DONE

    def canceled(self) -> bool:
        """
        Check if the task has finished successfully.
        """
        return self.status == self.meta.Status.CANCELED
