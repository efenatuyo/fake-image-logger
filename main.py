import discord
from flask import Flask, send_file, request
from discord.ext import commands
from threading import Thread
import configparser

app = Flask(__name__)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
config = configparser.ConfigParser(allow_no_value=True)
setup = configparser.ConfigParser()

config.read("database.ini")
website = "https://test.com/"
@app.route('/<value>')
def index(value):
    if str(value) in config["users"]:
        number = config[str(value)]["views"]
        config[str(value)]["views"] = str(int(number) + 1)
        with open('database.ini', 'w') as configfile:
          config.write(configfile)
    return send_file("Discord.png", mimetype='image/png')

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command(name="create_image")
async def create_image(ctx):
    if str(ctx.author.id) in config['users']:
         return await ctx.reply(embed=discord.Embed(title="**You already have a image please use `!delete_image` to to create a new image**", color=0xff0000))
    config['users'][f'{str(ctx.author.id)}'] = None
    config[f'{str(ctx.author.id)}'] = {}
    config[f'{str(ctx.author.id)}']['views'] = "0"
    with open('database.ini', 'w') as configfile:
             config.write(configfile)
    return await ctx.reply(embed=discord.Embed(title="**Succesfully setup image type `!logs` to see your logs and image link**", color=0x4dff00))

@bot.command(name="delete_image")
async def delete_image(ctx):
        if str(ctx.author.id) not in config['users']:
         return await ctx.reply(embed=discord.Embed(title="**You don't have a image yet use `!create_image` to create one**", color=0xff0000))
        config.remove_section(f"{str(ctx.author.id)}")
        config.remove_option("users", f"{str(ctx.author.id)}")
        with open('database.ini', 'w') as configfile:
          config.write(configfile)
        return await ctx.reply(embed=discord.Embed(title="**Succesfully removed image**", color=0x4dff00))

@bot.command(name="logs")
async def logs(ctx):
    if str(ctx.author.id) not in config['users']:
         return await ctx.reply(embed=discord.Embed(title="**You don't have a image yet use `!create_image` to create one**", color=0xff0000))
    embed=discord.Embed(title=f"**{ctx.author.name} logs**", color=0x4dff00)
    embed.add_field(name="Link to image", value=website+str(ctx.author.id), inline=False)
    embed.add_field(name="Total hits", value=config[str(ctx.author.id)]["views"], inline=True)
    embed.set_footer(text="pay to acces hits")
    return await ctx.reply(embed=embed)
    
def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()
bot.run('')