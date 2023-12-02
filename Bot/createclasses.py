# this model holds all the classse that the create view will use

import discord
from discord import ui 





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
                
        


#this is the modal for delting embeds
class CreatViewDeleteEmbedSelect(ui.Select):
    def __init__(self, view):
        options = []
        for i, embed in enumerate(view.embeds):
            options.append(discord.SelectOption(label=f"Embed {i}",value = i))
        
        super().__init__(placeholder="Select an embed to delete", options=options)

    async def callback(self, interaction):
        self.view.embeds.remove(self.view.embeds[int(self.values[0])])
        self.view.remove_item(self)

        # check if their are NO embeds and content
        if len(self.view.embeds)== 0 and self.view.content == None:
            self.view.children[2].disabled = True
            self.view.children[3].disabled = True
            await self.view.message.delete()
            self.view.message = None
        elif len(self.view.embeds) == 0:
            self.view.children[2].disabled = True
            self.view.children[3].disabled = True
        else: # otherwise just edit the message, this is to avoid sending an empty message
            await self.view.message.edit(embeds=self.view.embeds)
        await interaction.response.edit_message(view=self.view)


#the edit embed select view
# the way this works is, this will show a select menu of ALL the embeds you have, when you select one, it'll bring up the embed modal and use it to edit the embed
class CreateViewEmbedSelect(ui.Select):
    def __init__(self, view):
        options = []
        for i, embed in enumerate(view.embeds):
            options.append(discord.SelectOption(label=f"Embed {i}", value=i))
        super().__init__(placeholder="Select an embed to edit", options=options, min_values=0, max_values=1)
    
    async def callback(self, interaction:discord.Interaction):
        self.view.remove_item(self)
        if len(self.values) == 0:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(CreateViewEditEmbedModal(view=self.view, embed=self.values[0]))
        await interaction.edit_original_response(view=self.view)




# the modal for editing the messages content
class CreateViewContentModal(ui.Modal):
    def __init__(self, view:ui.View):
        super().__init__(title="Content Editor", timeout=300)
        self.view = view
        self.contentMessage.default = view.content

    contentMessage = ui.TextInput(label="Content", style=discord.TextStyle.paragraph, placeholder="The actual content to the message")
    

    async def on_submit(self, interaction:discord.Interaction):
        # vars the user can use
        
        

        # checks and balances
        if self.view.children[0].label == "Add Content": #change the label from add content to edit
            self.view.children[0].label = "Edit Content"
            self.view.children[4].disabled = False
            await interaction.response.edit_message(view=self.view) #edit the view
            if self.view.message == None: # if there isnt a "message object" yet, then create one
                self.view.message = await interaction.channel.send(self.contentMessage.value)
            else: #if there already is, then just set the content aspect   
                await self.view.message.edit(content=self.contentMessage.value)
        else:
            await interaction.response.defer(ephemeral=True)
            await self.view.message.edit(content=self.contentMessage.value)
            

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
        color = self.ecolor.value.replace("#", "")
        embed = discord.Embed(title=self.etitle.value, description=self.edescription.value, color=int(color, base=16))
        if self.view.message:
            self.view.embeds.append(embed)
            await self.view.message.edit(embeds=self.view.embeds)
        else:
            self.view.embeds.append(embed)
            self.view.message = await interaction.channel.send(embeds=self.view.embeds)
        self.view.children[2].disabled = False
        self.view.children[3].disabled = False
        await interaction.response.edit_message(view=self.view)