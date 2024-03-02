from discord import Interaction, Embed, ButtonStyle
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump

def commandFunction(tree, client):
    @tree.command(name="counter",description="Change the counter for gremlins (only use if it's really necessary)")
    @default_permissions(administrator=True)
    async def counterCommand(interaction: Interaction, counter: int):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
            return
        
        specialConfig["count"] = counter

        try:
            with open("specialConfig.json", "w") as specialConfigFile:
                dump(specialConfig, specialConfigFile, indent=4)
            embed = Embed(title=" ",description=f"**:white_check_mark: Successfully set the counter to {counter}**",colour=2067276)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(SUCCESS) Counter has been CHANGED")
        except:
            embed = Embed(title=" ",description="**:x: An error has occured while trying to modify the counter**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the counter")