# needs to be reworked

import discord
from discord.ext import commands
from discord import app_commands
import json
from levels import LevelFuncs



def addbal(uid, bal):
    f = open("eco.json")
    data = json.load(f)
    f.close()
    try: data["balance"][f"{uid}"] += bal
    except KeyError: data["balance"][f"{uid}"] = bal
    balance = data["balance"][f"{uid}"]
    f = open("eco.json", "w")
    json.dump(data, f)
    f.close()
    return balance


def getbal(uid):
    f = open("eco.json")
    data = json.load(f)
    f.close()
    try: bal = data["balance"][f"{uid}"]
    except KeyError: bal = 0
    return bal


class Eco(commands.Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(description="Check the balance of yourself or another user")
    async def bal(self, interaction:discord.Interaction, user:discord.Member=None):
        if not user: user = interaction.user
        bal = getbal(user.id)
        await interaction.response.send_message(f'the balance for {user.display_name} is {bal}')

    

    @app_commands.command(description="Work a job to make income")
    @app_commands.checks.cooldown(1, 120)
    async def work(self, interaction:discord.Interaction):
        data = LevelFuncs.getLevel(interaction.user.id)
        level = data["level"]
        xp = data["xp"]
        ammount = (level*100) + xp # the ammount the user earns
        LevelFuncs.editxp(interaction.user.id, 0)
        val = addbal(interaction.user.id, ammount)
        await interaction.response.send_message(f"You worked and made 💸`{ammount}` You now have 💸`{val}`\n(Level `{level}`*100 + `{xp}` xp)")

        
    @work.error
    async def work_error(self, interaction:discord.Interaction, error:app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(error, ephemeral=True)
    


    

    
class Gamble(commands.Cog):
    def __init__(self) -> None:
        super().__init__()



class Bumping(commands.Cog):
    def __init__(self) -> None:
        super().__init__()

    @commands.Cog.listener('on_message')
    async def bumplistener(self, msg:discord.Message):
        if msg.author.id == 302050872383242240:
            if msg.embeds and msg.embeds[0].url == "https://disboard.org/":
                user = msg.interaction.user # the user who bumped
                data = LevelFuncs.getLevel(user.id)
                level = data["level"]
                bal = addbal(user.id, level*100) # give the user cash
                
                await msg.channel.send(f"THANKS {user.mention} for bumping the server! you got 💸200! (You now have `{bal}`)")
        

    @app_commands.command()
    async def fakebump(self, interaction:discord.Interaction):
        embed = discord.Embed(title="DISBOARD: The Public Server List", description="Bump done! :thumbsup:\nCheck it out [on DISBOARD.](https://disboard.org/server/929889617128349758)", url="https://disboard.org/")
        embed.set_image(url="https://disboard.org/images/bot-command-image-bump.png")
        await interaction.response.send_message(embed=embed)

