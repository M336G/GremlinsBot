from discord import Interaction, Embed
from discord.app_commands import default_permissions
from util.functions import log
from datetime import datetime
from random import choice
from json import load, dump

def commandFunction(tree, client):
    @tree.command(name="gremlin",description="Manually tells the bot to post a gremlin (only use if it's really necessary)")
    @default_permissions(administrator=True)
    async def gremlinCommand(interaction: Interaction):
        # Check if the administrator is in Globed's Server, if it's the case it continues the command, otherwise it throws an error message
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to execute the gremlin command")
            return
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
            await interaction.response.send_message(" ", embed=embed, ephemeral=True)

        #images = []
        star_images = []
        #one_day_ago = datetime.now() - timedelta(days=1)

        # Check every messages sent in the gremlins channel, only get the ones that are images (also gets the message content and the author)
        async for message in gremlins_channel.history(): #after=one_day_ago
            for reaction in message.reactions:
                if str(reaction.emoji) == "⭐":
                    async for user in reaction.users():
                        member = await interaction.guild.fetch_member(user.id)  # get the Member object for the user
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

                embed3 = Embed(title=" ",description=f"**:white_check_mark: Successfully posted gremlin in <#{post_channel_id}>!**",colour=2067276)

                try:
                    await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
                    # And notifies the user who executed the command that a gremlin has successfully been posted in the daily channel
                    await interaction.response.send_message(" ", embed=embed3, ephemeral=True)
                # If it cannot, throws an error
                # Adds +1 to the Gremlin counter
                    try:
                        specialConfig["count"] = specialConfig["count"] + 1
                        with open("specialConfig.json", "w") as specialConfigFile:
                            dump(specialConfig, specialConfigFile, indent=4)
                        log(f"(SUCCESS) POSTED a gremlin")
                    except:
                        embed5 = Embed(title=" ",description=f"**:x: An error occured while trying to update the gremlins counter**", colour=15548997)
                        await interaction.response.send_message(" ", embed=embed5, ephemeral=True)
                except:
                    embed4 = Embed(title=" ",description=f"**:x: Could not post the message in the daily gremlins channel. Are you sure that the bot can send messages there?**", colour=15548997)
                    await interaction.response.send_message(" ", embed=embed4, ephemeral=True)
            
            # If it doesn't, it won't add a field
            else:
                # Embed content without description
                embed = Embed(title=f'Gremlin of the Day #{specialConfig["count"]}',description=f'**Submitted by <@{author.id}>**', colour=2123412)
                embed.set_image(url=f"{chosen_image}")
                embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
                embed.timestamp = datetime.now()

                # 2nd embed content
                embed2 = Embed(title=" ",description=f"**Submit your gremlins in <#{channel_id}>**", colour=3447003)

                embed3 = Embed(title=" ",description=f"**:white_check_mark: Successfully posted gremlin in <#{post_channel_id}>!**",colour=2067276)

                try:
                    await daily_gremlins_channel.send(" ", embeds=(embed, embed2))
                    # And notifies the user who executed the command that a gremlin has successfully been posted in the daily channel
                    await interaction.response.send_message(" ", embed=embed3, ephemeral=True)
                # If it cannot, throws an error
                # Adds +1 to the Gremlin counter
                    try:
                        specialConfig["count"] = specialConfig["count"] + 1
                        with open("specialConfig.json", "w") as specialConfigFile:
                            dump(specialConfig, specialConfigFile, indent=4)
                        log(f"(SUCCESS) POSTED a gremlin")
                    except:
                        embed5 = Embed(title=" ",description=f"**:x: An error occured while trying to update the gremlins counter**", colour=15548997)
                        await interaction.response.send_message(" ", embed=embed5, ephemeral=True)
                except:
                    embed4 = Embed(title=" ",description=f"**:x: Could not post the message in the daily gremlins channel. Are you sure that the bot can send messages there?**", colour=15548997)
                    await interaction.response.send_message(" ", embed=embed4, ephemeral=True)

        # Otherwise, it throws an error message
        else:
            embed = Embed(title="No images found!",description=f"**Could not find any images in <#{channel_id}> today**",colour=15548997)
            await interaction.response.send_message(" ", embed=embed, ephemeral=True)
            log(f"(FAILED) FAILED to post a gremlin")