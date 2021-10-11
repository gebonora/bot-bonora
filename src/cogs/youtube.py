import discord
from discord.ext import commands

from src.utils.mediaplayer import MediaPlayer

from src.utils.fileQueue import FileQueue


class Youtube(commands.Cog, name="Youtube"):

    def __init__(self, bot, file_queue):
        self.bot = bot
        self.file_queue = file_queue
        self.isPlaying = False

    @commands.command(name='play')
    async def play_music(self, ctx, url):
        print("Received URL " + url)

        server = self.get_server(ctx)
        await self.join(ctx)
        voice_channel = self.get_voice_client(ctx)

        try:
            async with ctx.typing():
                await self.file_queue.add_url(url)  # get from queue
                await self.start_music(ctx)
        except Exception as e:
            print(e)

    @commands.command(name='join')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} conectate al canal bro".format(ctx.message.author.name))
            return
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        except Exception as e:
            print(e)

    @commands.command(name='pause')
    async def pause(self, ctx):
        voice_client = self.get_voice_client(ctx)
        voice_client.pause()

    @commands.command(name='queue_info')
    async def queue_info(self, ctx):
        await ctx.send('Queue size: {}'.format(self.file_queue.size()))

    async def start_music(self, ctx):
        voice_client = self.get_voice_client(ctx)
        filename = self.file_queue.get_next()
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename), after=self.check_queue)
        await ctx.send('**Now playing:** {}'.format(filename))

    def check_queue(self, ctx):
        print("CHECKING QUEUE:")
        if not self.file_queue.is_empty():
            self.start_music(ctx)
        print("NO MORE MUSIC")

    def get_server(self, ctx):
        return ctx.message.guild

    def get_voice_client(self, ctx):
        return self.get_server(ctx).voice_client


def setup(bot):
    file_queue = FileQueue()
    bot.add_cog(Youtube(bot, file_queue))
