from discord import Client, Intents, ActivityType, Embed, Activity
from discord.app_commands import CommandTree, default_permissions
from util.resources import TOKEN
from util.functions import log 
from os import listdir
from os.path import isfile, join
from discord.ext import commands, tasks
import random
import json
import datetime
from datetime import timedelta

class aclient(Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.synced = False
        self.commands = {}
    
    async def on_ready(self):
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Logged in as {self.user}.")
        await client.change_presence(activity=Activity(type=ActivityType.watching, name="your gremlins"))
        log(f"(SUCCESS) {self.user} has been STARTED. Ping: {round (client.latency * 1000)} ms")

client = aclient()
tree = CommandTree(client)

for command in listdir("commands"):
    if (not(isfile(join("commands", command)))):
        continue

    module = __import__("commands." + command[:-3], fromlist=["commandFunction"])
    commandObject = client.commands[command] = globals()[module.__name__] = module
    commandObject.commandFunction(tree, client)

@tasks.loop(minutes=1)
async def image_rotate():
    with open("specialConfig.json", "r") as specialConfigFile:
        specialConfig = json.load(specialConfigFile)
        channel_id = specialConfig["gremlins_thread"]
        post_channel_id = specialConfig["daily_gremlins"]

    daily_gremlins_channel = client.get_channel(post_channel_id)
    gremlins_channel = client.get_channel(channel_id)

    if gremlins_channel is None:
        embed = Embed(title=" ",description=f"**:x: Could not find any gremlins channel. Are you sure you defined it, or does it exist?**")
        await daily_gremlins_channel.send(" ", embed=embed)
        return

    images = []
    one_day_ago = datetime.now() - timedelta(minutes=5)
    async for message in gremlins_channel.history(after=one_day_ago):
        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['.png', '.jpg', '.jpeg', '.gif', 'webp']):
                    images.append((attachment.url, message.content))

    if images:
        chosen_image, image_description, author = random.choice(images)
        if image_description:
            embed = Embed(title="Gremlin of the Day",description=f"**Submitted by {author.id}**\n'{image_description}'", colour=2123412)
            embed.set_image(url=f"{chosen_image}")
            embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
            embed.timestamp = datetime.now()

            embed2 = embed = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

            await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
        else:
            embed = Embed(title="Gremlin of the Day",description=f"**Submitted by {author.id}**", colour=2123412)
            embed.set_image(url=f"{chosen_image}")
            embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
            embed.timestamp = datetime.now()

            embed2 = embed = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

            await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
            log(f"(SUCCESS) POSTED a gremlin")
    else:
        embed = Embed(title="No images found!",description=f"**Could not find any images in <#{channel_id}>**",colour=15548997)
        await daily_gremlins_channel.send(" ", embed=embed)
        log(f"(FAILED) FAILED to post a gremlin")

client.run(TOKEN)