import asyncio

import discord
from discord.ext import commands

from src.utils.mediaplayer import MediaPlayer

from src.utils.fileQueue import FileQueue


class Youtube(commands.Cog, name="Youtube"):

    def __init__(self, bot, file_queue):
        self.bot = bot
        self.file_queue = file_queue
        self.paused_by_command = False

    @commands.command(name='play')
    async def play_music(self, ctx, url):
        print("Received URL " + url)

        server = self.get_server(ctx)
        await self.join(ctx)
        voice_client = self.get_voice_client(ctx)

        try:
            async with ctx.typing():
                await self.file_queue.add_url(url)
                await ctx.send("Song added to queue: {}".format(url))
            if not voice_client.is_playing():
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
        if voice_client.is_playing():
            voice_client.pause()
            self.paused_by_command = True
            await ctx.send("Paused by {}".format(ctx.message.author.name))
            return
        await ctx.send("There is nothing playing to pause")

    @commands.command(name='continue')
    async def continue_playing(self, ctx):
        voice_client = self.get_voice_client(ctx)
        if not self.paused_by_command:
            return
        voice_client.resume()
        self.paused_by_command = False

    @commands.command(name='queue_info')
    async def queue_info(self, ctx):
        await ctx.send('Queue size: {}'.format(self.file_queue.size()))

    async def start_music(self, ctx):
        voice_client = self.get_voice_client(ctx)
        filename = self.file_queue.get_next()
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                          after=lambda x: self.check_queue(ctx))
        await ctx.send('**Now playing:** {}'.format(filename))

    def check_queue(self, ctx):
        print("CHECKING QUEUE:")
        if not self.file_queue.is_empty():
            voice_client = self.get_voice_client(ctx)
            filename = self.file_queue.get_next()
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                              after=lambda x: self.check_queue(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."), self.bot.loop)

    def get_server(self, ctx):
        return ctx.message.guild

    def get_voice_client(self, ctx):
        return self.get_server(ctx).voice_client


def setup(bot):
    file_queue = FileQueue()
    bot.add_cog(Youtube(bot, file_queue))
