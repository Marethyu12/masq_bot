import discord
import requests

from bs4 import BeautifulSoup
from discord.ext import commands
from tdynws import get_content

cmd_prefix = "!masq "
token = "NjU0MTQzNzM1ODgxNDAwMzIx.XfBQ5A.dvoavyYMFuzb5J9Jp3e3-r0AR7E"
jimmys_id = 489987032920358922

client = commands.Bot(command_prefix=cmd_prefix)

client.remove_command("help")

@client.command(pass_context=True)
async def hi(ctx):
    await ctx.send("@" + ctx.message.author.name + ", hello")

@client.command(pass_context=True)
async def halpme(ctx):
    help_msg = ("**Usage:** !masq [command] [arguments]\n\n"
                 "**List of commands:**\n\n"
                 "`hi` Sends me a 'hi' message\n"
                 "`halpme` Displays this info\n"
                 "`tdynws` Fetches top news articles from Burnaby Now\n"
                 "`potassium` Make bot offline (Only Jimmy can use it due to obvious reasons)")
    
    await ctx.send(help_msg)

@client.command(pass_context=True)
async def tdynws(ctx):
    url = "https://www.burnabynow.com/news"
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    top_today_articles = soup.find(class_="leading-articles")
    
    for article in top_today_articles.find_all("article"):
        a = article.find("a")
        link = a["href"]
        
        try:
            await ctx.send(get_content(url[:-5] + link))
        except:
            continue

@client.command(pass_context=True)
async def potassium(ctx):
    if ctx.message.author.id == jimmys_id:
        await ctx.send("Goodbye!")
        await client.logout()
    else:
        await ctx.send("Goodbye! Wait... you are not Jimmy so never mind")

# TODO: math eval, tictactoe with minimax, random art

@client.event
async def on_ready():
    print("Logged in as Masquerade!")

client.run(token)