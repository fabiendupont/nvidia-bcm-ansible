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

import json
import logging


class InfoMessageCache:
    """
    Cache for the monitoring information messages
    """

    def __init__(self, cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self.messages = {}

    def ensure(self, message_keys):
        """
        Ensure the messages for the supplied list of message keys is in memory
        """
        new_message_keys = [it for it in message_keys if it not in self.messages]
        if len(new_message_keys) == 0:
            return 0
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getInfoMessages',
            args=[new_message_keys],
        )
        if code:
            self.logger.warning('Error retrieving info messages: %s', out)
        else:
            self.messages.update({it['key']: self._translate(it['message']) for it in out})
            self.logger.info('Got new info messages: %d / %d, %d', len(new_message_keys), len(message_keys), len(out))
        return len(out)

    def _translate(self, message):
        if len(message) > 0 and message[0] == '[' and message[-1] == ']':
            try:
                uuids = json.loads(message)
                entities = self.cluster.get_by_uuid(uuids)
                message = ', '.join([it.resolve_name for it in entities])
            except ValueError:
                pass
        return message

    def get(self, message_key):
        """
        Get the information messages linked to a message key.
        """
        return self.messages.get(message_key, None)
