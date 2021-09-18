import discord
from discord.ext import commands

from src.utils.mediaplayer import MediaPlayer


class Youtube(commands.Cog, name="Youtube"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play_music(self, ctx, url):
        print("Received URL " + url)

        try:

            server = ctx.message.guild
            await self.join(ctx)

            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await MediaPlayer.from_url(url, loop=False)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
            await ctx.send('**Now playing:** {}'.format(filename))
        except Exception as e:
            print(e)

    @commands.command(name='join')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} conectate al canal bro".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()


def setup(bot):
    bot.add_cog(Youtube(bot))
