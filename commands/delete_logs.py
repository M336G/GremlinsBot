from discord import Interaction, Embed, Member, Role
from discord.app_commands import default_permissions
from util.functions import log

def commandFunction(tree, client):
    @tree.command(name="delete_logs",description="A command used by M336 to clear the logs")
    @default_permissions(administrator=True)
    async def deleteLogsCommand(interaction: Interaction):
        if interaction.user.id != 629711559899217950:
            embed = Embed(title=" ",description="**:x: You cannot use this command!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        elif interaction.guild.id != 1189719927817519145:
            embed = Embed(title=" ",description="**:x: You cannot use this command here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
        else:
            try:
                log(f"(RESET) Logs have been RESET")
                embed = Embed(title=" ",description="**Logs have been reset!**",colour=2067276)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            except:
                embed = Embed(title=" ",description="**:x: An error has occured while trying to reset the logs**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
