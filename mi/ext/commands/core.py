import asyncio
from typing import Dict

from mi.ext.commands._types import _BaseCommand


class CommandManager:
    def __init__(self, *args, **kwargs):
        self.all_commands: Dict[str, Command] = {}
        super().__init__(*args, **kwargs)  # Clientクラスを初期化する

    def add_command(self, command: 'Command'):
        if not isinstance(command, Command):
            raise TypeError(f'{command}はCommandクラスである必要があります')

        self.all_commands[command.regex] = command


class Command(_BaseCommand):
    def __init__(self, func, regex: str, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'{func}はコルーチンでなければなりません')
        self.regex: str = regex
        self.callback = func

    async def invoke(self, ctx, *args, **kwargs):
        await self.callback(self, ctx, *args, **kwargs)


def mention_command(regex: str):
    def decorator(func, **kwargs):
        return Command(func, regex=regex, **kwargs)

    return decorator
