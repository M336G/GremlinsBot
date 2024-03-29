from discord import Interaction, Embed, TextChannel, Thread
from discord.app_commands import default_permissions
from util.functions import log
import json

def commandFunction(tree, client):
    @tree.command(name="gremlins_channel",description="Set the channel where gremlins should be taken from")
    @default_permissions(administrator=True)
    async def gremlinsThreadsChannelCommand(interaction: Interaction, channel: TextChannel = None, thread: Thread = None):
        if channel is not None or thread is not None:
            if channel is None and thread is not None:
                channel_id = thread.id
            if channel is not None and thread is None:
                channel_id = channel.id
            if interaction.guild.id != 1155027487957458974:
                embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
                return
            if channel is not None and thread is not None:
                embed = Embed(title=" ",description="**:x: You cannot set 2 channels at the same time!**",colour=15548997)
                await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Channel")
                return
            else: 
                with open("specialConfig.json", "r") as specialConfigFile:
                    data = json.load(specialConfigFile)

                if channel_id == data["gremlins"]:
                    embed = Embed(title=" ",description="**:x: This channel is already set!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Channel")
                    return
                if channel_id == data["daily_gremlins"]:
                    embed = Embed(title=" ",description="**:x: This channel is already set for daily gremlins!**",colour=15548997)
                    await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                    log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
                    return

                else:
                    data["gremlins"] = channel_id

                    try:
                        with open("specialConfig.json", "w") as specialConfigFile:
                            json.dump(data, specialConfigFile, indent=4)
                        embed = Embed(title=" ",description=f"**:white_check_mark: Successfully set the new gremlins channel to <#{channel_id}>**",colour=2067276)
                        await interaction.response.send_message(" ",embed=embed)
                        log(f"(SUCCESS) Gremlins Channel has been CHANGED")
                    except:
                        embed = Embed(title=" ",description="**:x: An error has occured while trying to set the new gremlins channel**",colour=15548997)
                        await interaction.response.send_message(" ",embed=embed, ephemeral=True)
                        log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Channel")
        else:
            embed = Embed(title=" ",description="**:x: You haven't defined any settings!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the Gremlins Channel")