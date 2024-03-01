from discord import Interaction, Embed, Member, Role, ButtonStyle
from discord.ui import Button, View
from util.functions import log

def commandFunction(tree, client):
    @tree.command(name="credits",description="Show the credits of the bot")
    async def creditsCommand(interaction: Interaction):
        embed = Embed(title=" ",description=f"<@1213101749758459935> has been created by <@629711559899217950> for **Globed**\n\nPFP by <@761897716187922453>",colour=2123412)
        
        button = Button(label='Support Globed', style=ButtonStyle.url, url='https://ko-fi.com/globed')
        view = View()
        view.add_item(button)

        log(f"(SUCCESS) {interaction.user} used /credits")

        await interaction.response.send_message(" ",embed=embed, view=view, ephemeral=True)