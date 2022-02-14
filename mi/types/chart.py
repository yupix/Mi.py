__all__ = ('ActiveUsersChartPayload',)

from typing import List, TypedDict, Union


class ActiveUsersChartPayload(TypedDict):
    read_write: List[int]
    read: List[int]
    write: List[int]
    registered_within_week: List[Union[int]]
    registered_within_month: List[int]
    registered_within_year: List[int]
    registered_outside_week: List[int]
    registered_outside_month: List[int]
    registered_outside_year: List[int]
