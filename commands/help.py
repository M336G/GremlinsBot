from discord import Interaction, Embed, Member, Role, ButtonStyle 
from discord.app_commands import default_permissions, ContextMenu, CommandTree
from discord.ui import Button, View
from util.functions import log

commandsDetails:object = {}

def commandFunction(tree:CommandTree, client):
    @tree.command(name="help",description="Show all the commands")
    async def helpCommand(interaction: Interaction):
        
        if len(commandsDetails) <= 0:
            #D Give an array of all commands
            commands:[] = await tree.fetch_commands()
            if commands == None:
                commands = tree.get_commands()
            for elt in commands:
                if isinstance(elt, ContextMenu):
                    continue

                id:int = 0
                description:str = ""
                try:
                    id = elt.id
                    description = elt.description
                except AttributeError:
                    id = id
                    description = description
                
                commandsDetails[elt.name] = {"description": elt.description, "id": id}

        commandList = ["help", "ping", "credits", "gremlin", "daily_gremlins_channel", "gremlins_channel"]

        def getFieldContentCommand(name:str):
            response:[] = [f"/{name}", "", False]

            command = commandsDetails[name]
            if not(command == None): 
                id:int = 0
                description:str = ""
                try:
                    id = command['id']
                    description = command['description']
                except AttributeError:
                    id = id
                    description = description
                
                response = [f"</{name}:{id}>", f"\n{description}", False]
            return response

        def addFieldToEmbed(embed, commandList): 
            for commandName in commandList:
                commandAttribute:[] = getFieldContentCommand(commandName)
                embed.add_field(name=commandAttribute[0], value=commandAttribute[1], inline=commandAttribute[2])


        embed = Embed(title="Bot commands",description="", colour=2123412)
        embed.add_field(name="\n__Commands__", value="", inline=False)
        addFieldToEmbed(embed, commandList)

        embed2 = Embed(title=f" ",description="<@1213101749758459935> has been created by <@629711559899217950> for **Globed**",colour=2123412)
        
        button = Button(label='Support Globed', style=ButtonStyle.url, url='https://ko-fi.com/globed')
        view = View()
        view.add_item(button)
        await interaction.response.send_message(" ", embeds=(embed, embed2), view=view)
        #await interaction.channel.send(" ",, view=view)

        log(f"(SUCCESS) {interaction.user} used /help")
