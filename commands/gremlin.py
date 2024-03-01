from discord import Interaction, Embed
from util.functions import log
from json import load
from random import choice
from json import load
from datetime import timedelta, datetime

def commandFunction(tree, client):
    @tree.command(name="gremlin",description="Manually tells the bot to post a gremlin (only use if it's really necessary)")
    async def gremlinCommand(interaction: Interaction):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
            channel_id = specialConfig["gremlins"]

            if channel_id == "null":
                channel_id = specialConfig["gremlins"]
                if channel_id == "null":
                    return
        
            post_channel_id = specialConfig["daily_gremlins"]

            if post_channel_id == "null":
                post_channel_id = specialConfig["daily_gremlins"]
                if post_channel_id == "null":
                    return

        daily_gremlins_channel = client.get_channel(post_channel_id)
        gremlins_channel = client.get_channel(channel_id)

        if gremlins_channel is None:
            embed = Embed(title=" ",description=f"**:x: Could not find any gremlins channel. Are you sure you defined it, or does it exist?**")
            await interaction.response.send_message(" ", embed=embed, ephemeral=True)
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

            embed = Embed(title="Gremlin of the Day",description=f"**Submitted by <@{author.id}>**\n{image_description}", colour=2123412)
            embed.set_image(url=f"{chosen_image}")
            embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
            embed.timestamp = datetime.now()

            embed2 = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

            await daily_gremlins_channel.send(" ", embeds=(embed, embed2))

            embed3 = Embed(title=" ",description=f"**:white_check_mark: Successfully posted gremlin in <#{post_channel_id}>!**",colour=2067276)
            await interaction.response.send_message(" ", embed=embed3, ephemeral=True)
            log(f"(SUCCESS) POSTED a gremlin")
        else:
            embed = Embed(title="No images found!",description=f"**Could not find any images in <#{channel_id}> today**",colour=15548997)
            await interaction.response.send_message(" ", embed=embed, ephemeral=True)
            log(f"(FAILED) FAILED to post a gremlin")