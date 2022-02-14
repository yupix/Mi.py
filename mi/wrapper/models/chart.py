__all__ = ('RawActiveUsersChart')

from typing import List

from mi.types.chart import ActiveUsersChartPayload


class RawActiveUsersChart:
    __slots__ = (
        'read_write',
        'read',
        'write',
        'registered_within_week',
        'registered_within_month',
        'registered_within_year',
        'registered_outside_week',
        'registered_outside_month',
        'registered_outside_year',
    )

    def __init__(self, data: ActiveUsersChartPayload):
        self.read_write: List[int] = data['read_write']
        self.read: List[int] = data['read']
        self.write: List[int] = data['write']
        self.registered_within_week = data['registered_within_week']
        self.registered_within_month = data['registered_within_month']
        self.registered_within_year = data['registered_within_year']
        self.registered_outside_week = data['registered_outside_week']
        self.registered_outside_month = data['registered_outside_month']
        self.registered_outside_year = data['registered_outside_year']
