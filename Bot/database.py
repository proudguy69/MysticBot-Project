# this will contain class and methods to set up and alter the postgres database

# tables for the database are created locally in PG admin

import asyncpg
import json
import discord
from discord import app_commands
from discord.ext import commands


f = open('../settings.json')
data = json.load(f)
password = data["DBKEY"]



class Database():
    # this will be ran when the bot joins a server, needs to create all tables for said server
    async def createServer(sid):
        conn = await asyncpg.connect(host="127.0.0.1", port=1101, user="postgres", password=password, database="main")
        await conn.execute("INSERT INTO servers(SID) VALUES($1)", sid)
        await conn.execute("INSERT INTO welcome_conf(SID) VALUES($1)", sid)

    

    # this is bad database design and class design, but this is currently here as example
    # async def createWelcome_Conf(sid, content):
    #    conn = await asyncpg.connect(host="127.0.0.1", port=1101, user="postgres", password=password, database="main")
    #    await conn.execute("INSERT INTO welcome_conf(SID, content) VALUES($1, $2)", sid, content)

