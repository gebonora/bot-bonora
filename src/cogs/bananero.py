import random

from discord.ext import commands


class Bananero(commands.Cog, name="Bananero"):
    mythical_phrases = [
        "El peluca sapeeee",
        "Quisiéramos usar tu lanchota",
        "Te voy a hacer cagar camuflado",
        "Esto es por meterte con mi zona, mi cabe-zona",
        "Putas Harry, putas!",
        "Que telaraña, tela-chupo!",
        "Ayy saliste putazo como la abuela!",
        "Apurate Harry que la negra nos hace dos por uno",
        "Sapeeeeeee"
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sape')
    async def sape(self, ctx):
        response = random.choice(self.mythical_phrases)
        await ctx.send(response)

    @commands.command(name="lokita")
    async def is_lokita(self, ctx):
        author = ctx.author.nick or ctx.author.name
        response = self.get_message(author)
        await ctx.send(response)

    @staticmethod
    def get_message(author):
        if random.random() < 0.5:
            return f'Efectivamente {author}, estás como lokita!!'
        else:
            return f'Me informan que {author} NO está como lokita'


def setup(bot):
    bot.add_cog(Bananero(bot))
