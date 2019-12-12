import discord
from discord.ext import commands

cmd_prefix = "!masq "
token = "NjU0MTQzNzM1ODgxNDAwMzIx.XfBQ5A.dvoavyYMFuzb5J9Jp3e3-r0AR7E"

client = commands.Bot(command_prefix=cmd_prefix)

client.remove_command("help")

@client.command(pass_context=True)
async def hi(ctx):
    await ctx.send(ctx.message.author.name + "...")

@client.command(pass_context=True)
async def intro(ctx):
    intro_msg = ("Hi I am Masquerade a general-purpose Discord bot. I am maintained and developed by JY.\n\n"
                 "**Usage:** !masq [command] [arguments]\n\n"
                 "**List of commands:**\n"
                 "`hi` Sends me a 'hi' message."
                 "`intro' Introduces myself"
                 "`potassium` (Only JY can use it) Make bot offline")
    
    await ctx.send(intro_msg)

@client.command(pass_context=True)
async def potassium(ctx):
    if ctx.message.author.id is not "489987032920358922":
        return
    
    await client.logout()

@client.event
async def on_ready():
    print("Logged in as Masquerade!")

client.run(token)