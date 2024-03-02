from discord import Client, Intents, ActivityType, Embed, Activity
from discord.app_commands import CommandTree
from util.resources import TOKEN
from util.functions import log 
from os import listdir
from os.path import isfile, join
from discord.ext import tasks
from random import choice
from json import load, dump
from datetime import datetime, timedelta

class aclient(Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.synced = False
        self.commands = {}
        self.context_menus = {}
    
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

for command in listdir("context_menu"):
    if (not(isfile(join("context_menu", command)))):
        continue
            
    module = __import__("context_menu." + command[:-3], fromlist=["commandFunction"])  # Remove the .py extension
    commandObject = client.context_menus[command] = globals()[module.__name__] = module
    commandObject.commandFunction(tree, client)

@tasks.loop(seconds=5)
async def image_rotate():
    if datetime.now().hour == 18 and datetime.now().minute == 00 and datetime.now().second <= 5:
        # Check if the administrator is in Globed's Server, if it's the case it continues the command, otherwise it throws an error message
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        # Open the specialConfig.json file and get every value
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
            channel_id = specialConfig["gremlins"]
            post_channel_id = specialConfig["daily_gremlins"]

            if channel_id == "null":
                channel_id = specialConfig["gremlins"]
                if channel_id == "null":
                    return
        
            if post_channel_id == "null":
                post_channel_id = specialConfig["daily_gremlins"]
                if post_channel_id == "null":
                    return

        # Get the channels based on their IDs, if it cannot then it throws an error
        try:
            daily_gremlins_channel = client.get_channel(post_channel_id)
            gremlins_channel = client.get_channel(channel_id)

        except:
            embed = Embed(title=" ",description=f"**:x: Could not find any gremlins channel. Are you sure you defined it, or does it exist?**", colour=15548997)
            await daily_gremlins_channel.send(" ", embed=embed)

        #images = []
        star_images = []

        one_day_ago = datetime.now() - timedelta(days=1)
        # Check every messages sent in the gremlins channel, only get the ones that are images (also gets the message content and the author)
        async for message in gremlins_channel.history(after=one_day_ago):
            for reaction in message.reactions:
                if str(reaction.emoji) == "⭐":
                    async for user in reaction.users():
                        guild = await client.fetch_guild(specialConfig["guild"])
                        member = await guild.fetch_member(user.id)  # get the Member object for the user
                        if any(role.id == specialConfig["gremlin_role"] for role in member.roles):
                            if message.attachments:
                                for attachment in message.attachments:
                                    if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['.png', '.jpg', '.jpeg', '.gif', 'webp']):
                                        star_images.append((attachment.url, message.content, message.author))

        # If there are images, the commands continues
        if star_images:
            chosen_image, image_description, author = choice(star_images)
            # If there is a description, add a field for it
            if image_description: 
                # Embed content w/ description
                embed = Embed(title=f'Gremlin of the Day #{specialConfig["count"]}',description=f'**Submitted by <@{author.id}>**', colour=2123412)
                embed.add_field(name=' ', value=f'"{image_description}"', inline=False)
                embed.set_image(url=f"{chosen_image}")
                embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
                embed.timestamp = datetime.now()
                # 2nd embed content
                embed2 = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

                try:
                    await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
                
                    try:
                        # Tries to add +1 to the Gremlin counter
                        specialConfig["count"] = specialConfig["count"] + 1
                        with open("specialConfig.json", "w") as specialConfigFile:
                            dump(specialConfig, specialConfigFile, indent=4)
                        log(f"(SUCCESS) POSTED a gremlin")
                    except:
                        # If it cannot, throws an error
                        print("An error occured while trying to update the gremlins counter") 
                except:
                    print("Could not post the message in the daily gremlins channel. Are you sure that the bot can send messages there?") 
            
            # If it doesn't, it won't add a field
            else:
                # Embed content without description
                embed = Embed(title=f'Gremlin of the Day #{specialConfig["count"]}',description=f'**Submitted by <@{author.id}>**', colour=2123412)
                embed.set_image(url=f"{chosen_image}")
                embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
                embed.timestamp = datetime.now()

                # 2nd embed content
                embed2 = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

                try:
                    await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
                    try:
                        # Tries to add +1 to the counter
                        specialConfig["count"] = specialConfig["count"] + 1
                        with open("specialConfig.json", "w") as specialConfigFile:
                            dump(specialConfig, specialConfigFile, indent=4)
                        log(f"(SUCCESS) POSTED a gremlin")
                    except:
                        # If it cannot, throws an error
                        print("An error occured while trying to update the gremlins counter") 
                except:
                    print("Could not post the message in the daily gremlins channel. Are you sure that the bot can send messages there?") 

        # Otherwise, it throws an error message
        else:
            embed = Embed(title="No images found!",description=f"**Could not find any images in <#{channel_id}>**",colour=15548997)
            await daily_gremlins_channel.send(" ", embed=embed)
            log(f"(FAILED) FAILED to post a gremlin (no images found)")

client.run(TOKEN)