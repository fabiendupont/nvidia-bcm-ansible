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

import typing

from pythoncm.entity.entity import Entity

if typing.TYPE_CHECKING:
    from uuid import UUID


class DrainResult(Entity):
    def _get_with_states(self, states: list[int]) -> list[UUID]:
        return [node_uuid for node_uuid, state in zip(self.ref_node_uuids, self.result) if state in states]

    def get_drained(self) -> list[UUID]:
        return self._get_with_states(
            [
                self.meta.Result.DRAINED,
                self.meta.Result.DRAINING,
            ]
        )

    def get_fully_drained(self) -> list[UUID]:
        return self._get_with_states(
            [
                self.meta.Result.DRAINED,
            ]
        )

    def get_unknown(self) -> list[UUID]:
        return self._get_with_states(
            [
                self.meta.Result.NOTANODE,
                self.meta.Result.INVALID,
                self.meta.Result.FAILED,
                self.meta.Result.UNKNOWN,
            ]
        )

    @property
    def all_drained(self) -> bool:
        return all(state in {self.meta.Result.DRAINED, self.meta.Result.NOTANODE} for state in self.result)
