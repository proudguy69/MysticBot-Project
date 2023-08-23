# this is to be worked on another day

import discord
from discord import app_commands
from discord.ext import commands

chats = [
    
]

messages = [
    
]

class Anonymous(commands.Cog):
    def __init__(self):
        super().__init__()
    
    #make it run in dms
    @app_commands.command(name='anonymous-chat')
    async def anomchat(self, interaction:discord.Interaction):
        #check if there are any chats awaiting a user
        for chat in chats:
            if len(chat['users']) == 1:
                # connect the user to this chat
                chat['users'].append(interaction.user.id)
                if interaction.channel_id == 894918681476358174: await interaction.response.send_message("You have entered a chat! say hi!")
                else: interaction.response.send_message("You have entered a chat, Say hi! (in dms you dimwit)", ephemeral=True)
                return
        chats.append({"id":len(chats)+1, "users":[interaction.user.id]})
        if interaction.channel_id != 894918681476358174: msg = await interaction.user.send("Created a chat! Connecting you to another user...");await interaction.response.send_message(f"Creating a chat! ({msg.jump_url})", ephemeral=True)
        else: msg = await interaction.response.send_message("Created a chat! Connecting you to another user...")
        
        
    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        pass
        
        
        
        
        
        