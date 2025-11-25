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

from datetime import datetime
from datetime import timedelta


class Request:
    def __init__(self):
        self.group_by_user = False
        self.group_by_group = False
        self.group_by_account = False
        self.group_by_job_name = False
        self.group_by_job_id = False
        self.group_by_accounting_info = []
        self.users = []
        self.groups = []
        self.accounts = []
        self.job_names = []
        self.job_ids = []
        self.accounting_info = None
        self.period_start = 0
        self.period_end = 0
        self.start = 0
        self.limit = 1000
        self.include_running_jobs = False
        self.calculate_prediction = False

    def __start_end(self, time_offset):
        if isinstance(time_offset, tuple):
            return time_offset
        return time_offset, 1

    def period(
        self,
        day: int | None = 0,
        week: int | None = None,
        month: int | None = None,
        quarter: int | None = None,
        year: int | None = None,
        calculate_prediction: bool = False,
    ):
        now = datetime.now()
        if year is not None:
            start, end = self.__start_end(year)
            self.period_start = datetime(now.year, 0, 0) + timedelta(years=start)
            self.period_end = self.period_start + timedelta(years=end) - timedelta(seconds=1)
        elif quarter is not None:
            start, end = self.__start_end(month)
            quarter_month = (now.month - 1) % 3
            self.period_start = datetime(now.year, now.month, 0) + timedelta(months=start - quarter_month)
            self.period_end = self.period_start + timedelta(months=end - quarter_month) - timedelta(seconds=1)
        elif month is not None:
            start, end = self.__start_end(month)
            self.period_start = datetime(now.year, now.month, 0) + timedelta(months=start)
            self.period_end = self.period_start + timedelta(months=end) - timedelta(seconds=1)
        elif week is not None:
            start, end = self.__start_end(week)
            week_day = now.weekday()
            self.period_start = datetime(now.year, now.month, now.day) + timedelta(days=start * 7 - week_day)
            self.period_end = self.period_start + timedelta(days=end * 7) - timedelta(seconds=1)
        else:
            start, end = self.__start_end(day)
            self.period_start = datetime(now.year, now.month, now.day) + timedelta(days=start)
            self.period_end = self.period_start + timedelta(days=end) - timedelta(seconds=1)
        if not calculate_prediction and self.period_end > now:
            self.period_end = now
        self.period_start = int(self.period_start.timestamp())
        self.period_end = int(self.period_end.timestamp())
        return self.period_start < self.period_end

    def today(self, calculate_prediction: bool = False):
        self.include_running_jobs = True
        self.calculate_prediction = calculate_prediction
        return self.period(day=0, calculate_prediction=calculate_prediction)

    def yesterday(self, calculate_prediction: bool = False):
        self.include_running_jobs = False
        return self.period(day=-1)

    def this_week(self, calculate_prediction: bool = False):
        self.include_running_jobs = True
        self.calculate_prediction = calculate_prediction
        return self.period(week=0, calculate_prediction=calculate_prediction)

    def last_week(self, calculate_prediction: bool = False):
        self.include_running_jobs = False
        return self.period(week=-1)

    def this_month(self, calculate_prediction: bool = False):
        self.include_running_jobs = True
        self.calculate_prediction = calculate_prediction
        return self.period(month=0, calculate_prediction=calculate_prediction)

    def last_month(self, calculate_prediction: bool = False):
        self.include_running_jobs = False
        return self.period(month=-1)

    def this_year(self, calculate_prediction: bool = False):
        self.include_running_jobs = True
        self.calculate_prediction = calculate_prediction
        return self.period(year=0, calculate_prediction=calculate_prediction)

    def last_year(self, calculate_prediction: bool = False):
        self.include_running_jobs = False
        return self.period(year=-1)
