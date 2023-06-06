import discord
import json
import os
from dotenv import load_dotenv
from discord.ext import commands

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
target_id: int = int(data["target_id"])


# cooldown for on_message events
cd_mapping = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        bucket = cd_mapping.get_bucket(message)
        assert bucket is not None

        retry_after = bucket.update_rate_limit()

        if retry_after:
            return
        else:
            if message.author.id == target_id and message.content.strip() in key_words:
                print(f"Message from {message.author}: {message.content}")
                await message.channel.send(
                    f"{message.author.mention} {message.content}"
                )


def main():
    client = MyClient(intents=intents)
    client.run(TOKEN)


main()
