import discord
from discord.ext import commands
import asyncio
import wavelink


class Lava(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        """Simple play command"""
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            vc: wavelink.Player = ctx.voice_client
        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(track)
        else:
            await vc.put_wait(track)
            await vc.channel.send(f"Queued: {track.title}")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackEventPayload):
        vc: wavelink.Player = payload.player
        vc.channel.send(content=f"Now playing: {payload.track.title}")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        vc: wavelink.Player = payload.player
        if vc.queue.is_empty:
            return
        track = await vc.queue.get_wait()
        await vc.play(track)

    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        """Simple disconnect command"""

        if ctx.voice_client:
            vc: wavelink.Player = ctx.voice_client
            await vc.disconnect()


async def setup(bot: commands.Bot):
    node: wavelink.Node = wavelink.Node(
        uri="http://localhost:2333", password="youshallnotpass"
    )
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    await bot.add_cog(Lava(bot))
