import discord
import json
import os
import logging
import re
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands


INLINE_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FOOTNOTE_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\[(\d+)\]")
FOOTNOTE_LINK_URL_RE = re.compile(r"\[(\d+)\]:\s+(\S+)")

# setup logger
logger = logging.getLogger("discord")
logging.basicConfig(level=logging.NOTSET)


# load env variables
load_dotenv()
TOKEN = os.getenv("TOKEN") or ""

# loads words from target user to look out for
f = open("config.json")
data = json.load(f)
f.close()
key_words: dict[str, str] = data["key_words"]


class customBot(commands.Bot):
    def __init__(self) -> None:
        # discord intents
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            intents=intents, command_prefix=commands.when_mentioned_or("$")
        )

    def find_md_links(self, md):
        """Return dict of links in markdown"""

        links = list(INLINE_LINK_RE.findall(md))
        footnote_links = dict(FOOTNOTE_LINK_TEXT_RE.findall(md))
        footnote_urls = dict(FOOTNOTE_LINK_URL_RE.findall(md))

        for key in footnote_links.keys():
            links.append((footnote_links[key], footnote_urls[footnote_links[key]]))

        return links

    async def on_ready(self) -> None:
        logging.info(f"Logged on as {self.user} | {self.user.id}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user or message.author.bot == True:
            return
        if message.content.strip().lower() in key_words.keys():
            logging.info(msg=f"Message from {message.author}: {message.content}")
            await message.channel.send(f"{key_words[message.content.strip().lower()]}")

        links = self.find_md_links(message.content.strip())
        if links:
            logging.info(msg=f"Links detected: {links}")
            await message.channel.send(
                f"Links detected:\n" + "\n".join([str(x) for x in links])
            )

        await bot.process_commands(message)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            path = Path(filename)
            if path.suffix == ".py":
                await self.load_extension(f"cogs.{path.stem}")
                logging.info(f"Loaded cogs.{path.stem}")


bot = customBot()


bot.run(token=TOKEN)
