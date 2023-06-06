import discord
import json
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands

# setup logger
logger = logging.getLogger("discord")
logging.basicConfig(level=logging.NOTSET)

# discord intents
intents = discord.Intents.default()
intents.message_content = True

# load env variables
load_dotenv()
TOKEN = os.getenv("TOKEN") or ""

# loads words from target user to look out for
f = open("config.json")
data = json.load(f)
f.close()
key_words: list[str] = data["key_words"]


class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(msg=f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.strip().lower() in key_words:
            logging.info(msg=f"Message from {message.author}: {message.content}")
            await message.channel.send(f"{message.content.strip().lower()}")


def main():
    client = MyClient(intents=intents)
    client.run(TOKEN)


main()
