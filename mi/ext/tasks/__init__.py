import asyncio
from typing import Any, Callable, Coroutine, Dict, Optional
from mi.exception import TaskNotRunningError

__all__ = ["Loop", "loop"]



class Loop:
    def __init__(self, func: Callable[..., Coroutine[Any, Any, Any]], seconds: int = 60):
        self.seconds: int = seconds
        self.func: Callable[..., Coroutine[Any, Any, Any]] = func
        self._task: Optional[asyncio.Task] = None
        self.stop_next_iteration = None

    def start(self, *args: tuple[Any], **kwargs: Dict[Any, Any]) -> asyncio.Task:
        """
        タスクを開始する

        Parameters
        ----------
        args : Any
        kwargs : Any

        Returns
        -------
        _task : asyncio.Task
        """
        _loop = asyncio.get_running_loop()
        self._task = _loop.create_task(self.task(*args, **kwargs))
        return self._task

    def stop(self):
        """
        タスクを停止

        Returns
        -------
        None

        """
        if self._task is None:
            raise TaskNotRunningError('タスクは起動していません')

        if not self._task.done():
            self.stop_next_iteration = True

    async def task(self, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        while True:
            if self.stop_next_iteration:
                return
            await self.func(self.seconds, *args, **kwargs)
            await asyncio.sleep(self.seconds)


def loop(n: int):
    def _deco(f: Callable[..., Coroutine[Any, Any, Any]]) -> Loop:
        return Loop(f, n)

    return _deco
