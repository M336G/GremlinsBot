from discord import Interaction, Embed
from util.functions import log
from json import load

def commandFunction(tree, client):
    @tree.command(name="list",description="Show how much gremlins have been submitted")
    async def listCommand(interaction: Interaction):
        with open("specialConfig.json", "r") as specialConfigFile:
            specialConfig = load(specialConfigFile)
            channel_id = specialConfig["gremlins"]
        if interaction.guild.id != specialConfig["guild"]:
            embed = Embed(title=" ",description="**:x: You cannot use this here!**",colour=15548997)
            await interaction.response.send_message(" ",embed=embed, ephemeral=True)
            log(f"(FAILED) {interaction.user} FAILED to change the Daily Gremlins Channel")
            return
        
        try:
            gremlins_channel = client.get_channel(channel_id)

        except:
            embed = Embed(title=" ",description=f"**:x: Could not find any gremlins channel. Are you sure you defined it, or does it exist?**", colour=15548997)
            await interaction.response.send_message(" ", embed=embed, ephemeral=True)

        counter = 1
        embeds = [Embed(title=f"Submissions",description=" ",colour=2123412)]

        #try:
        await interaction.response.defer(ephemeral=True)
        star_images = []
        async for message in gremlins_channel.history():
            for reaction in message.reactions:
                if str(reaction.emoji) == "⭐":
                    async for user in reaction.users():
                        member = await interaction.guild.fetch_member(user.id)
                        if any(role.id == specialConfig["gremlin_role"] for role in member.roles):
                            if message.attachments:
                                for attachment in message.attachments:
                                    if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['.png', '.jpg', '.jpeg', '.gif', 'webp']):
                                        star_images.append((message.content, message.jump_url))

        for image_description, message_url in star_images:
            if len(embeds[-1].fields) == 25:  # Check if the last embed is full
                embeds.append(Embed(title=f"Submissions (cont.)",description=" ",colour=2123412))  # Create a new embed if it's the case
            
            if image_description:
                embeds[-1].add_field(name=f'Submission #{counter}', value=f'"{image_description}"\n{message_url}', inline=False)
                counter += 1
            else:
                embeds[-1].add_field(name=f'Submission #{counter}', value=f'{message_url}', inline=False)
                counter += 1
        await interaction.response.edit_original_response(embeds=embeds) # Sends all the embeds

        #except:
            #embed = Embed(title=" ",description=f"**:x: An error occured while trying to display the list of gremlins**", colour=15548997)
            #await interaction.response.send_message(" ", embed=embed, ephemeral=True)