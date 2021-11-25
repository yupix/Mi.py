import asyncio

__all__ = ["Loop", "loop"]


class Loop:
    def __init__(self, func, seconds=None):
        self.seconds = seconds
        self.func = func
        self._task = None
        self.stop_next_iteration = None

    def start(self, *args, **kwargs) -> asyncio.Task:
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
        if not self._task.done():
            self.stop_next_iteration = True

    async def task(self, *args, **kwargs):
        while True:
            if self.stop_next_iteration:
                return
            await self.func(self.seconds, *args, **kwargs)
            await asyncio.sleep(self.seconds)


def loop(n):
    def _deco(f):
        return Loop(f, n)

    return _deco
