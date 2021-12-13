from typing import Any, Dict

from mi.abc.ext.context import AbstractContext


class Context(AbstractContext):
    def __init__(self, **attrs: Any):
        self.message = attrs.pop("message", None)
        self.bot = attrs.pop("bot", None)
        self.command = attrs.pop("command", None)

    async def invoke(self, command, /, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        arguments = []
        if command.cog is not None:
            arguments.apped(command.cog)
        arguments.append(self)
        arguments.extend(args)

        ret = await command.callback(*arguments, **kwargs)
        return ret
