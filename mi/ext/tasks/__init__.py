import asyncio
import datetime
from typing import Any, Callable, Coroutine, Dict, Optional, Sequence, Union

from mi.exception import TaskNotRunningError
from mi.utils import MISSING

__all__ = ["Loop", "loop"]


class Loop:
    def __init__(self, coro: Callable[..., Coroutine[Any, Any, Any]],
                 seconds: float,
                 hours: float,
                 minutes: float,
                 time: Union[datetime.time, Sequence[datetime.time]],
                 count: Optional[int],
                 custom_loop: Optional[asyncio.AbstractEventLoop] = None):
        self.seconds: float = seconds
        self.hours: float = hours
        self.minutes: float = minutes
        self.time: Union[datetime.time, Sequence[datetime.time]] = time
        self.count: Optional[int] = count
        self.coro: Callable[..., Coroutine[Any, Any, Any]] = coro
        self._task: Optional[asyncio.Task[Any]] = None
        self.stop_next_iteration = None
        self.loop: Optional[asyncio.AbstractEventLoop] = custom_loop
        self.sleep_time = datetime.timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours)).total_seconds()
        self.error_coro = None

    def start(self, *args, **kwargs) -> asyncio.Task[Any]:
        """
        タスクを開始する

        Parameters
        ----------
        args : Any
        kwargs : Any

        Returns
        -------
        _task : asyncio.Task[Any]
        """

        _loop = asyncio.get_event_loop() if self.loop is None else self.loop
        self._task = _loop.create_task(self._loop(*args, **kwargs))
        return self._task

    def stop(self):
        """
        タスクを停止
        """

        if self._task is None:
            raise TaskNotRunningError('タスクは起動していません')

        if not self._task.done():
            self.stop_next_iteration = True

    async def _loop(self, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        while True:
            if self.stop_next_iteration:
                return
            try:
                await self.coro(*args, **kwargs)
            except Exception as e:
                await self.error_coro(e)
            await asyncio.sleep(self.sleep_time)

    def error(self, func):
        self.error_coro = func


def loop(
        *,
        seconds: float = MISSING,
        minutes: float = MISSING,
        hours: float = MISSING,
        time: Union[datetime.time, Sequence[datetime.time]] = MISSING,
        count: Optional[int] = None,
        custom_loop: Optional[asyncio.AbstractEventLoop] = None
):
    def decorator(func):
        return Loop(
            func,
            seconds,
            minutes,
            hours,
            time,
            count,
            custom_loop=custom_loop
        )

    return decorator
