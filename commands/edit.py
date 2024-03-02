from discord import Interaction, Embed
from discord.app_commands import default_permissions
from util.functions import log
from json import load

def commandFunction(tree, client):
    @tree.command(name="edit",description="Edit one of the message the bot posted")
    @default_permissions(administrator=True)
    async def editCommand(interaction: Interaction, quote: str, message_id: str):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to edit a message")
            return
        
        try:
            with open("specialConfig.json", "r") as specialConfigFile:
                data = load(specialConfigFile)
                
        except:
                embed = Embed(title=" ",description="**:x: An error occured while trying to open the config file**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to edit a message (could not open specialConfig.json)")

        try:
            channel = client.get_channel(data["daily_gremlins"])
            message = await channel.fetch_message(int(message_id))
        
            old_embed = message.embeds[0]
            old_embed2 = message.embeds[1]

            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=old_embed.color)
            
            embed.add_field(name=' ', value=f'{quote}', inline=False)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{client.user.name} Bot", icon_url=f"{client.user.avatar}")
            embed.timestamp = old_embed.timestamp

            embed2 = Embed(title=old_embed2.title, description=old_embed2.description, color=old_embed2.color)

            await message.edit(embeds=(embed, embed2))
            embed = Embed(title=" ",description=f"**:white_check_mark: Successfully edited the message!**",colour=2067276)
            await interaction.response.send_message(" ", embed=embed, ephemeral=True)
            log(f"(SUCCESS) EDITED a message")
            
        except:
            embed = Embed(title=" ",description="**:x: An error occured while trying to modify the message**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to edit a message")