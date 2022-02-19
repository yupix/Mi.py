from mi.ext import commands


class BasicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.mention_command(text='hello')
    async def hello(self, ctx: commands.Context):
        await ctx.message.reply('Hello! %s' % ctx.author.name)


def setup(bot: commands.Bot):
    bot.add_cog(BasicCog(bot))
