from discord.ext import commands


class Basic(commands.Cog, name="Basic"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("bonora_bot has started...")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        message.content = message.content.lower()
        if message.content == "hello bot":
            if str(message.author) == "RolandKa#5398":
                await message.channel.send("My creator salutes me! Hello my lord!")
            else:
                await message.channel.send("Hello")


def setup(bot):
    bot.add_cog(Basic(bot))
