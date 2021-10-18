import asyncio
from time import sleep

import discord
from discord.ext import commands

from src.utils.mediaplayer import MediaPlayer

from src.utils.fileQueue import FileQueue

# TODO: add help description for commands
# TODO: add youtube searching to play command


SAME_CHANNEL_MESSAGE = "tenés que estar en el mismo canal que el bot para enviar el comando"
NO_CHANNEL_MESSAGE = "conectate a un canal bro"


class Youtube(commands.Cog, name="Youtube"):

    def __init__(self, bot, file_queue):
        self.bot = bot
        self.file_queue = file_queue
        self.paused_by_command = False

    @commands.command(name='play', aliases=['p'])
    async def play_music(self, ctx, *args):
        if not ctx.message.author.voice:
            await ctx.send("{} {}".format(ctx.message.author.nick, NO_CHANNEL_MESSAGE))
            return
        if not args:
            await self.continue_playing(ctx)
            return

        url = args[0]
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
            await ctx.send("{} {}".format(ctx.message.author.nick, NO_CHANNEL_MESSAGE))
            return
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        except Exception as e:
            print(e)

    @commands.command(name='leave')
    async def leave(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} {}".format(ctx.message.author.nick, NO_CHANNEL_MESSAGE))
            return
        try:
            await self.get_voice_client(ctx).disconnect()
        except Exception as e:
            print(e)

    @commands.command(name='pause')
    async def pause(self, ctx):
        if not self.is_bot_and_author_in_same_channel(ctx):
            await ctx.send("{} {}".format(ctx.message.author.nick, SAME_CHANNEL_MESSAGE))
            return
        voice_client = self.get_voice_client(ctx)
        if voice_client.is_playing():
            voice_client.pause()
            self.paused_by_command = True
            await ctx.send("Paused by {}".format(ctx.message.author.nick))
            return
        await ctx.send("There is nothing playing to pause")

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx):
        if not self.is_bot_and_author_in_same_channel(ctx):
            await ctx.send("{} {}".format(ctx.message.author.nick, SAME_CHANNEL_MESSAGE))
            return
        voice_client = self.get_voice_client(ctx)
        voice_client.pause()
        await ctx.send("Skipping song...")
        self.check_queue(ctx)

    @commands.command(name='queue_info')
    async def queue_info(self, ctx):
        await ctx.send('Queue size: {}'.format(self.file_queue.size()))

    @commands.command(name='erase')
    async def erase(self, ctx):
        if not self.is_bot_and_author_in_same_channel(ctx):
            await ctx.send("{} {}".format(ctx.message.author.nick, SAME_CHANNEL_MESSAGE))
            return
        voice_client = self.get_voice_client(ctx)
        voice_client.pause()
        try:
            self.file_queue.clear()
        except Exception as e:
            print(e)
        await ctx.send("Queue cleared!")

    async def start_music(self, ctx):
        voice_client = self.get_voice_client(ctx)
        filename = self.file_queue.get_next()
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                          after=lambda x: self.check_queue(ctx))
        await ctx.send('**Now playing:** {}'.format(filename))

    async def continue_playing(self, ctx):
        voice_client = self.get_voice_client(ctx)
        if not self.paused_by_command:
            return
        voice_client.resume()
        self.paused_by_command = False

    def check_queue(self, ctx):
        print("CHECKING QUEUE:")
        voice_client = self.get_voice_client(ctx)
        if not self.file_queue.is_empty():
            filename = self.file_queue.get_next()
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                              after=lambda x: self.check_queue(ctx))
        else:
            sleep(25)
            if voice_client and not voice_client.is_playing():
                asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."), self.bot.loop)
                asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop)

    def get_server(self, ctx):
        return ctx.message.guild

    def get_voice_client(self, ctx):
        return self.get_server(ctx).voice_client

    def is_bot_and_author_in_same_channel(self, ctx):
        author_voice = ctx.message.author.voice
        bot_voice = self.get_voice_client(ctx)
        return author_voice and bot_voice and author_voice.channel == bot_voice.channel


def setup(bot):
    file_queue = FileQueue()
    bot.add_cog(Youtube(bot, file_queue))
