import discord

from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a channel"""
        vc: discord.VoiceClient = ctx.voice_client
        if vc is not None:
            return await vc.move_to(channel)
        await channel.connect()

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects bot"""
        vc: discord.VoiceClient = ctx.voice_client
        await vc.disconnect()


async def setup(bot):
    await bot.add_cog(Music(bot))
