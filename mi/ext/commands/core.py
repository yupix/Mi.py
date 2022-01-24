import asyncio
from typing import List, Optional

from mi.ext.commands._types import _BaseCommand


class CMD:
    def __init__(self, cmd_type: str, key: str, func: 'Command'):
        self.cmd_type = cmd_type
        self.key = key
        self.func = func


class CommandManager:
    def __init__(self, *args, **kwargs):
        self.all_commands: List[CMD] = []
        super().__init__(*args, **kwargs)  # Clientクラスを初期化する

    def add_command(self, command: 'Command'):
        if not isinstance(command, Command):
            raise TypeError(f'{command}はCommandクラスである必要があります')
        command_type = 'regex' if command.regex else 'text'
        command_key = command.regex or command.text
        self.all_commands.append(CMD(command_type, command_key, command))


class Command(_BaseCommand):
    def __init__(self, func, regex: str, text: str, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f'{func}はコルーチンでなければなりません')
        self.regex: str = regex
        self.text: str = text
        self.callback = func

    async def invoke(self, ctx, *args, **kwargs):
        await self.callback(self, ctx, *args, **kwargs)


def mention_command(regex: Optional[str] = None, text: Optional[str] = None):
    def decorator(func, **kwargs):
        return Command(func, regex=regex, text=text, **kwargs)

    return decorator
