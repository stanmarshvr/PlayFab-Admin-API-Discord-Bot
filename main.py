import discord
from discord.ext import commands
import requests
import json
import re 


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

target_role_id = config.get('allowed_role_id')
print(config.get('allowed_role_id'))

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all(), help_command=None) 



@bot.hybrid_command(name="help", description="Show's what the bot can do.")
async def help(ctx):
    await ctx.send("# Hey! Welcome to my Bot\nMade By JTMC\n# ❗❗❗ALERT! YOU WILL NEED THE ROLE ID IN ORDER TO USE THESE COMMANDS❗❗❗\n\n\n/ban <player_id> <reason> <DurationInHours> This Simply Bans a user from your playfab title\n\n/delete_player <player_id>. This deletes the Master Player Account in your playfab title.")




@bot.event
async def on_ready():
    print("Your bot is online and ready (logged in as {bot.user.name})")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
    await bot.tree.sync() #sync the command tree
    print("Bot is ready and online")


def make_playfab_request(path, payload=None, method='post'):
    url = f'https://{config["playfab_title_id"]}.playfabapi.com/{path}'
    headers = {
        'X-SecretKey': config["playfab_secret_key"],
        'Content-Type': 'application/json'
    }

    if method == 'post':
        response = requests.post(url, json=payload, headers=headers)
    elif method == 'get':
        response = requests.get(url, headers=headers)
    else:
        return None

    return response.json()

def is_allowed_role(ctx):
    allowed_role_id = int(config["allowed_role_id"])
    return any(role.id == allowed_role_id for role in ctx.author.roles)

def get_content_inside_brackets(input_string):
    content_inside_brackets = input_string.split('[')

    if len(content_inside_brackets) > 1:
        # Split again to get the content inside the brackets
        content = content_inside_brackets[1].split(']')[0]
        return content
    else:
        return None

@bot.hybrid_command(name="ban", description="Ban's a User from PlayFab")
async def ban(ctx, player_id : str , reason : str , length : int):
    payload = {
        "Bans": [{        
        'DurationInHours': length,
        'Reason': reason,
        'PlayFabId': player_id
        }]
    }
    

    # Check if the user has the specified role
    if discord.utils.get(ctx.author.roles, id=target_role_id):
        embed = discord.Embed(title="Processing Your Request",
                      description="This Could Take A While...",
                      colour=0x9a0e95)

        embed.set_author(name="Playfab Fella",
                 url="https://www.youtube.com/",
                 icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")

        message = await ctx.send(embed=embed)
        response = make_playfab_request('Admin/BanUsers', payload)
        if response and not response.get('200'):
            embed2 = discord.Embed(title="Success!",
                      description=f'Succesfully Banned {player_id} for {length} due to {reason}',
                      colour=0x00ff4c)

            embed2.set_author(name="Playfab Fella",
                 url="https://www.youtube.com/",
                 icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")
            await message.edit(embed = embed2)
        else:
            await ctx.send('Failed to ban the player.')
    else:
        embed3 = discord.Embed(title="Error!",
                      description=f'You dont have the required role',
                      colour=0xff0000)

        embed3.set_author(name="Playfab Fella",
                 url="https://www.youtube.com/",
                 icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")
        await ctx.send(embed = embed3)
    
    




@bot.hybrid_command(name="delete_player", description="Deletes a Master Player Account")
async def delete_player(ctx, player_id: str):
    if discord.utils.get(ctx.author.roles, id=target_role_id):
        payload = {
        'PlayFabId': player_id
        }

        embed = discord.Embed(title="Processing Your Request",
                          description="This Could Take A While...",
                          colour=0x9a0e95)

        embed.set_author(name="Playfab Fella",
                     url="https://www.youtube.com/",
                     icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")

        message = await ctx.send(embed=embed)
        response = make_playfab_request('Admin/DeleteMasterPlayerAccount', payload)
        print(response)
        response_str = json.dumps(response)
        response_content = get_content_inside_brackets(response_str)
    

        if response.get('200'):
            embed2 = discord.Embed(title="Success!",
                               description=f'Successfully Deleted {player_id}',
                               colour=0x00ff4c)

            embed2.set_author(name="Playfab Fella",
                          url="https://www.youtube.com/",
                          icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")
            await message.edit(embed=embed2)
        else:
            if response.get('error'):
                embed3 = discord.Embed(title="Error!",
                                   description=f'Failed to delete master player account\nReason: {response_content}',
                                   colour=0xff0000)

                embed3.set_author(name="Playfab Fella",
                              url="https://www.youtube.com/",
                              icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")
            await message.edit(embed=embed3)
    else:
        embed4 = discord.Embed(title="Error!",
                      description=f'You dont have the required role',
                      colour=0xff0000)

        embed4.set_author(name="Playfab Fella",
                 url="https://www.youtube.com/",
                 icon_url="https://i.ibb.co/stPtTcw/2023-12-01-0ih-Kleki.png")
        await ctx.send(embed = embed4)





bot.run(config["discord_bot_token"])