from discord import Interaction, Embed, TextChannel, Thread
from discord.app_commands import default_permissions
from util.functions import log
from json import load, dump

def commandFunction(tree, client):
    @tree.command(name="daily_gremlins_channel",description="Set the channel where gremlins should be posted everyday")
    @default_permissions(administrator=True)
    async def dailyGremlinsChannelCommand(interaction: Interaction, channel: TextChannel = None, thread: Thread = None):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
            return
        if channel is not None or thread is not None:
            if channel is None and thread is not None:
                channel_id = thread.id
            if channel is not None and thread is None:
                channel_id = channel.id
            if channel is not None and thread is not None:
                embed = Embed(title=" ",description="**:x: You cannot set 2 channels at the same time!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
                return
            else: 
                if channel_id == specialConfig["daily_gremlins"]:
                    embed = Embed(title=" ",description="**:x: This channel is already set!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
                    return
                if channel_id == specialConfig["gremlins"]:
                    embed = Embed(title=" ",description="**:x: This channel is already set for gremlins!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
                    return

                else:
                    specialConfig["daily_gremlins"] = channel_id

                    try:
                        with open("specialConfig.json", "w") as specialConfigFile:
                            dump(specialConfig, specialConfigFile, indent=4)
                        embed = Embed(title=" ",description=f"**:white_check_mark: Successfully set the new daily gremlins channel to <#{channel_id}>**",colour=2067276)
                        await interaction.response.send_message(" ",embed=embed)
                        log(f"(SUCCESS) Daily Gremlins Channel has been CHANGED")
                    except:
                        embed = Embed(title=" ",description="**:x: An error has occured while trying to set the new daily gremlins channel**",colour=15548997)
                        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                        log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")

        else:
            embed = Embed(title=" ",description="**:x: You haven't defined any settings!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")