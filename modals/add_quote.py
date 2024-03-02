from discord.ui import Modal, TextInput
from discord import Embed, TextStyle, Interaction, Message
from util.functions import log

class add_quote_form(Modal, title='Add Quote'):
    def __init__(self, client, message: Message):
        self.client = client
        self.message = message
        super().__init__()
    input_0 = TextInput(label="Add Quote",placeholder="Add a quote to the message",style=TextStyle.long, required=False)
    async def on_submit(self, interaction: Interaction):
        try:
            message = await interaction.channel.fetch_message(self.message.id)
        
            old_embed = message.embeds[0]
            old_embed2 = message.embeds[1]

            embed = Embed(title=old_embed.title, description=f'{old_embed.description}', color=old_embed.color)
            
            embed.add_field(name=' ', value=f'{self.input_0}', inline=False)
            embed.set_image(url=old_embed.image.url)
            embed.set_footer(text=f"{self.client.user.name} Bot", icon_url=f"{self.client.user.avatar}")
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