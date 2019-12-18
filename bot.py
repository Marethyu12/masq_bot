import asyncio
import discord
import json
import requests

from bs4 import BeautifulSoup
from discord.ext import commands
from tdynws import get_content
from tictactoe import GameController
from ep import MiniLexer, ExpressionParser

dct = None

with open("data.json", "r") as json_file:
    dct = json.load(json_file)

cmd_prefix = "!masq "
token = dct["bot_token"]
jimmys_id = dct["jimmys_id"]

client = commands.Bot(command_prefix=cmd_prefix)

client.remove_command("help")

@client.command(pass_context=True)
async def hi(ctx):
    await ctx.send(ctx.message.author.name + ", hello")

@client.command(pass_context=True)
async def halpme(ctx):
    help_msg = ("**Usage:** `!masq [command] [optional arguments]`\n\n"
                 "**List of commands:**\n\n"
                 "- `hi` Send me a 'hi' message.\n\n"
                 "- `halpme` Display this info.\n\n"
                 "- `tdynws` Fetch top news articles from Burnaby Now.\n\n"
                 "- `tictactoe` `[difficulty]` Play a game of Tic Tac Toe with me.\n   difficulty options: `1` for easy `2` for medium `3` for hard `4` for impossible\n   example: `!masq tictactoe 4`\n\n"
                 "- `eval` `[math expression]` Evaluates and returns the final value of the given expression.\n   example: `!masq eval 3 * (1 / (5 - -pow(1.034, exp(2.01))) * atan(0.1)) + log2(30.1)`\n   supported functions: `pow`, `sqrt`, `abs`, `floor`, `ceil`, `log2`, `log10`, `exp`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`\n\n"
                 "- `potassium` Make bot offline. (Only Jimmy can use it due to obvious reasons)\n")
    
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
async def tictactoe(ctx, arg):
    difficulty = int(arg)
    
    if difficulty < 1 or difficulty > 4:
        await ctx.send("The difficulty is out of range please try again")
        return
    
    gc = GameController("X", difficulty)
    
    await ctx.send("**GAME START!**\n_ _")
    await ctx.send("To enter your move, input it in this format: `[row] [col]`. Note that the index of the top left square is `(0, 0)` and the index of the bottom right square is `(2, 2)`.\nYou have a minute to make a move.\nType \"I QUIT!\" to quit the game!\n_ _")
    await ctx.send(gc.board)
    
    def check(author):
        def inner_check(message):
            if message.author != author:
                return False
            try:
                inpt = message.content
                
                if inpt == "I QUIT!":
                    return True
                
                if len(inpt) is not 3:
                    return False
                
                r, c = int(inpt[0]), int(inpt[2])
                
                if r < 0 or r > 2 or c < 0 or c > 2:
                    return False
                
                return True
            except:
                return False
        return inner_check
    
    while not gc.game_over:
        try:
            await ctx.send("_ _\nEnter your move:")
            
            msg = await client.wait_for('message', check=check(ctx.author), timeout=60)
            
            if msg.content == "I QUIT!":
                break
            
            row, col = int(msg.content[0]), int(msg.content[2])
            gc.make_move(row, col)
            
            val = gc.check_win()
            
            if val is not None:
                if val == "T":
                    await ctx.send("Tie!\n_ _")
                else:
                    await ctx.send(val + " wins!\n_ _")
            
            await ctx.send(gc.board)
        except asyncio.TimeoutError:
            break
    
    gc.board.reset()
    
    await ctx.send("_ _\n**GAME OVER!**")

@client.command(pass_context=True)
async def eval(ctx, *args):
    await ctx.send("`" + str(ExpressionParser(MiniLexer(" ".join(args))).parse()) + "`")

@client.command(pass_context=True)
async def potassium(ctx):
    if ctx.message.author.id == jimmys_id:
        await ctx.send("Goodbye!")
        await client.logout()
    else:
        await ctx.send("Goodbye! Oh wait... you're not Jimmy so never mind")

# TODO: randomart, fetchmemes (get and post top 3 reddit memes; might be helpful: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html), bot description

@client.event
async def on_command_error(ctx, error):
    await ctx.send("``` ERROR: " + str(error) + "```")

client.run(token)
