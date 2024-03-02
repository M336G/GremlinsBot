from discord import Interaction, Embed, Role
from util.functions import log
from json import load, dump

def commandFunction(tree, client):
    @tree.command(name= "role", description="Set the role for people to react with stars")
    async def roleCommand(interaction: Interaction, role: Role):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Role")
            return

        else:
            if role.id == specialConfig["gremlin_role"]:
                embed = Embed(title=" ",description="**:x: This role is already set!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Role")
                return

            else:
                specialConfig["gremlin_role"] = role.id

                try:
                    with open("specialConfig.json", "w") as specialConfigFile:
                        dump(specialConfig, specialConfigFile, indent=4)
                    embed = Embed(title=" ",description=f"**:white_check_mark: Successfully set the new gremlins role to <@&{role.id}>**",colour=2067276)
                    await interaction.response.send_message(" ",embed=embed)
                    log(f"(SUCCESS) Gremlins Role has been CHANGED")
                except:
                    embed = Embed(title=" ",description="**:x: An error has occured while trying to set the new gremlins role**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Role")