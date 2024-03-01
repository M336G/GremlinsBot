from discord import Client, Intents, ActivityType, Embed, Activity
from discord.app_commands import CommandTree, default_permissions
from util.resources import TOKEN
from util.functions import log 
from os import listdir
from os.path import isfile, join
from discord.ext import commands, tasks
from random import choice
from json import load
from datetime import timedelta, datetime

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
        await image_rotate.start()

client = aclient()
tree = CommandTree(client)

for command in listdir("commands"):
    if (not(isfile(join("commands", command)))):
        continue

    module = __import__("commands." + command[:-3], fromlist=["commandFunction"])
    commandObject = client.commands[command] = globals()[module.__name__] = module
    commandObject.commandFunction(tree, client)

@tasks.loop(seconds=5)
async def image_rotate():
    if datetime.now().hour == 17 and datetime.now().minute == 0 and datetime.now().second <= 5:
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
            channel_id = specialConfig["gremlins"]
            # Check if the channel is a thread if not check if it's a channel then if doesn't exists return
            if channel_id == "null":
                channel_id = specialConfig["gremlins"]
                if channel_id == "null":
                    return
        
            post_channel_id = specialConfig["daily_gremlins"]
            # Check if the channel is a thread if not check if it's a channel then if doesn't exists return
            if post_channel_id == "null":
                post_channel_id = specialConfig["daily_gremlins"]
                if post_channel_id == "null":
                    return

        daily_gremlins_channel = client.get_channel(post_channel_id)
        gremlins_channel = client.get_channel(channel_id)

        if gremlins_channel is None:
            embed = Embed(title=" ",description=f"**:x: Could not find any gremlins channel. Are you sure you defined it, or does it exist?**")
            await daily_gremlins_channel.send(" ", embed=embed)
            return

        images = []
        one_day_ago = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 17, 0, 0)
        async for message in gremlins_channel.history(after=one_day_ago):
            if message.attachments:
                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['.png', '.jpg', '.jpeg', '.gif', 'webp']):
                        images.append((attachment.url, message.content, message.author))

        if images:
            chosen_image, image_description, author = choice(images)
            #if image_description:
            embed = Embed(title="Gremlin of the Day",description=f"**Submitted by <@{author.id}>**\n{image_description}", colour=2123412)
            embed.set_image(url=f"{chosen_image}")
            embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
            embed.timestamp = datetime.now()

            embed2 = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

            await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
            #else:
                # embed = Embed(title="Gremlin of the Day",description=f"**Submitted by {author.id}**", colour=2123412)
                #embed.set_image(url=f"{chosen_image}")
                #embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
                #embed.timestamp = datetime.now()

            #embed2 = embed = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

            #await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
            log(f"(SUCCESS) POSTED a gremlin")
        else:
            embed = Embed(title="No images found!",description=f"**Could not find any images in <#{channel_id}> today**",colour=15548997)
            await daily_gremlins_channel.send(" ", embed=embed)
            log(f"(FAILED) FAILED to post a gremlin")

client.run(TOKEN)