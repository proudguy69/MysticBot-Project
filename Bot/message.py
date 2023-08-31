# this is gonna be the module for our "Message Creator", where you can create, edit, and delete custom messages w/ embeds
import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.interactions import Interaction



from database import Database




class MessageGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="message", description="Commands to create, edit, and delete custom messages")



class Message(commands.Cog):
    def __init__(self) -> None:
        super().__init__()
    # Variables
    g = MessageGroup()




    # the view class for the creation tool
    class CreateView(ui.View):
        def __init__(self):
            super().__init__(timeout=300)
            self.message:discord.Message = None
            self.content:str = None
            self.embeds = []
    

        # the modal for editing a selected embed
        class CreateViewEditEmbedModal(ui.Modal):
            def __init__(self, view, embed):
                super().__init__(title="Embed Editor", timeout=300)
                embed = int(embed)
                self.view = view
                self.embed = embed
                
                self.etitle.default=view.embeds[embed].title
                self.edescription.default=view.embeds[embed].description
                self.ecolor.default=str(view.embeds[embed].color)
                # modal params
            etitle = ui.TextInput(label="title", style=discord.TextStyle.short, placeholder="The title of the embed")
            edescription = ui.TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="The desciption of the embed")
            ecolor = ui.TextInput(label="color", style=discord.TextStyle.short, placeholder="The desciption of the embed", required=False)
                
            async def on_submit(self, interaction:discord.Interaction):
                color = self.ecolor.value.replace("#", "")
                embed = discord.Embed(title=self.etitle.value, description=self.edescription.value, color=int(color, base=16))
                self.view.embeds[self.embed] = embed
                await self.view.message.edit(embeds=self.view.embeds)
                await interaction.response.defer()
                


        
        #the edit embed select view
        # the way this works is, this will show a select menu of ALL the embeds you have, when you select one, it'll bring up the embed modal and use it to edit the embed
        class CreateViewEmbedSelect(ui.Select):
            def __init__(self, view):
                options = []
                for i, embed in enumerate(view.embeds):
                    options.append(discord.SelectOption(label=f"Embed {i}", value=i))
                super().__init__(placeholder="Select an embed to edit", options=options, min_values=0, max_values=1)
            
            async def callback(self, interaction:discord.Interaction):
                if len(self.values) == 0:
                    await interaction.response.defer()
                else:
                    await interaction.response.send_modal(self.view.CreateViewEditEmbedModal(view=self.view, embed=self.values[0]))






        # the modal for editing the messages content
        class CreateViewContentModal(ui.Modal):
            def __init__(self, view:ui.View):
                super().__init__(title="Content Editor", timeout=300)
                self.view = view
                self.contentMessage.default = view.content

            contentMessage = ui.TextInput(label="Content", style=discord.TextStyle.paragraph, placeholder="The actual content to the message")
            

            async def on_submit(self, interaction:discord.Interaction):
                # vars the user can use
                user = interaction.user
                server = interaction.guild

                # checks and balances
                if self.view.children[0].label == "Add Content": #change the label from add content to edit
                    self.view.children[0].label = "Edit Content"
                    await interaction.response.edit_message(view=self.view) #edit the view
                    if self.view.message == None: # if there isnt a "message object" yet, then create one
                        self.view.message = await interaction.channel.send(self.contentMessage.value)
                    else: #if there already is, then just set the content aspect   
                        await self.view.message.edit(content=self.contentMessage.value.format(user=user,server=server))
                else:
                    await interaction.response.defer(ephemeral=True)
                    await self.view.message.edit(content=self.contentMessage.value.format(user=user,server=server))
                    

                # Change the Views data
                self.view.content = self.contentMessage.value

                        

        # the embed editor
        class CreateViewEmbedModal(ui.Modal):
            def __init__(self, view):
                super().__init__(title="Embed Editor", timeout=300)
                self.view = view
            etitle = ui.TextInput(label="title", style=discord.TextStyle.short, placeholder="The title of the embed")
            edescription = ui.TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="The desciption of the embed")
            ecolor = ui.TextInput(label="color", style=discord.TextStyle.short, placeholder="The desciption of the embed", required=False, default="000000") 
        
            async def on_submit(self, interaction:discord.Interaction):
                user = interaction.user
                server = interaction.guild
                embed = discord.Embed(title=self.etitle.value.format(user=user, server=server), description=self.edescription.value.format(user=user, server=server), color=int(self.ecolor.value, base=16))
                if self.view.message:
                    self.view.embeds.append(embed)
                    await self.view.message.edit(embeds=self.view.embeds)
                else:
                    self.view.embeds.append(embed)
                    self.view.message = await interaction.channel.send(embeds=self.view.embeds)
                self.view.children[2].disabled = False
                await interaction.response.edit_message(view=self.view)




        # the button to add content
        @ui.button(label="Add Content", style=discord.ButtonStyle.green)
        async def CreateViewAddContent(self, interaction:discord.Interaction, button:discord.Button):
            global content
            modal = self.CreateViewContentModal(self)
            await interaction.response.send_modal(modal)
            
            


        # the button to add embeds
        @ui.button(label="Add Embed", style=discord.ButtonStyle.green)
        async def CreateViewAddEmbed(self, interaction:discord.Interaction, button:discord.Button):
            # self.remove_item() # Need to add the select menu to the views varible so we can remove it once this is pressed
            await interaction.response.send_modal(self.CreateViewEmbedModal(self))


        # the button to edit embeds
        @ui.button(label="Edit Embeds", style=discord.ButtonStyle.green, disabled=True)
        async def CreateViewEditEmbeds(self, interaction:discord.Interaction, button:discord.Button):
            self.add_item(self.CreateViewEmbedSelect(self))
            await interaction.response.edit_message(view=self)

        # the button to edit embeds
        @ui.button(label="Delete Embeds", style=discord.ButtonStyle.red, disabled=True)
        async def CreateViewDeleteEmbeds(self, interaction:discord.Interaction, button:discord.Button):
            await interaction.response.defer()


        

    # The create command
    @g.command(name="create", description="Create a custom message")
    @app_commands.describe(name="The saved name of the message, you will use this to locate and use the message you create")
    async def create(self, interaction:discord.Interaction, name:str):
        embed = discord.Embed(title="Message Creator", description="Welcome to the message creator! Use the Buttons below to interact with the message below!")
        await interaction.response.send_message(embed=embed)
        await interaction.edit_original_response(view=self.CreateView())