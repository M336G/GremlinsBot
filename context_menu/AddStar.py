from discord import Interaction, Embed, Message
from discord.app_commands import default_permissions
from util.functions import log
from json import load

def commandFunction(tree, client):
    @tree.context_menu(name="Add Star")
    async def addStar(interaction:Interaction, message: Message):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)

        member = await interaction.guild.fetch_member(interaction.user.id)

        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to star a message (not in the good server)")
            return

        elif not any(role.id == specialConfig["gremlin_role"] for role in member.roles):
            embed = Embed(title=" ",description="**:x: You cannot use this!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to star a message (no gremlin role)")
            return
        
        
        
        else:
            message = await interaction.channel.fetch_message(message.id)
            try:
                if interaction.channel.id != specialConfig["gremlins"]:
                    embed = Embed(title=" ",description="**:x: You cannot star this message, since it is not in the gremlins channel!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to star a gremlin")
                elif any(reaction.emoji == "⭐" for reaction in message.reactions):
                    embed = Embed(title=" ",description="**:x: This message was already starred!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to star a gremlin")
                elif not any(attachment.filename.lower().endswith(image_ext) for attachment in message.attachments for image_ext in ['.png', '.jpg', '.jpeg', '.gif', 'webp']):
                    embed = Embed(title=" ",description="**:x: You cannot star this message, since it is not an image!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to star a gremlin")
                else:
                    await message.add_reaction('⭐')
                    embed = Embed(title=" ",description=f"**:white_check_mark: Successfully starred this gremlin!\n{message.jump_url}**",colour=2067276)
                    await interaction.response.send_message(" ", embed=embed, ephemeral=True)
                    log(f"(SUCCESS) STARRED a gremlin")
            except:
                embed = Embed(title=" ",description="**:x: An error occured while trying to star this gremlin**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to star a gremlin")