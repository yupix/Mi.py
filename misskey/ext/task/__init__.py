import asyncio


class Loop(object):
    def __init__(self, func, seconds=None):
        self.seconds = seconds
        self.func = func

    def start(self, *args, **kwargs):
        _loop = asyncio.get_event_loop()
        return _loop.create_task(self.task(*args, **kwargs))

    async def task(self, *args, **kwargs):
        while True:
            await self.func(self.seconds, *args, **kwargs)
            await asyncio.sleep(self.seconds)


def loop(n):

    def _deco(f):
        return Loop(f, n)

    return _deco
