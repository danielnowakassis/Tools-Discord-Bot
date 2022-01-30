from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="thelp")
    async def thelp(self, ctx):
        await ctx.send(
            """
            ```Tools Discord Bot```

            Comandos:

            `!timgtotxt` -> envie uma imagem(.png, .jpg) com comentário `!timgtotxt`, e o bot irá mandar sua imagem formada por caractéres ("#$%¨&*()").
"""
        )


def setup(bot):
    bot.add_cog(Help(bot))
