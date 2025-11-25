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

import signal
import threading


class GracefulInterruptHandler:
    def __init__(self):
        self.condition = threading.Condition()

    def __enter__(self):
        self.released = False

        self.original_sighup_handler = signal.getsignal(signal.SIGHUP)
        self.original_sigint_handler = signal.getsignal(signal.SIGINT)
        self.original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        def sighup_handler(signum, frame):
            self.wakeup()

        def sigint_handler(signum, frame):
            self.release()

        def sigterm_handler(signum, frame):
            self.release()

        signal.signal(signal.SIGHUP, sighup_handler)
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigterm_handler)
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def wakeup(self):
        with self.condition:
            if self.released:
                return False
            self.condition.notify_all()
            return None

    def release(self):
        with self.condition:
            if self.released:
                return False
            self.released = True
            self.condition.notify_all()

        signal.signal(signal.SIGHUP, self.original_sighup_handler)
        signal.signal(signal.SIGINT, self.original_sigint_handler)
        signal.signal(signal.SIGTERM, self.original_sigterm_handler)
        return True
