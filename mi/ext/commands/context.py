class Context:
    def __init__(self, **attrs):
        self.message = attrs.pop("message", None)
        self.bot = attrs.pop("bot", None)
        self.command = attrs.pop("command", None)

    async def invoke(self, command, /, *args, **kwargs):
        arguments = []
        if command.cog is not None:
            arguments.apped(command.cog)
        arguments.append(self)
        arguments.extend(args)

        ret = await command.callback(*arguments, **kwargs)
        return ret
