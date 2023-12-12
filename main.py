import discord
from discord.ext import commands
import requests
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix='!')

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

@bot.command()
@commands.check(is_allowed_role)
async def ban(ctx, player_id, reason, length):
    payload = {
        'BannedUntil': length,
        'BanReason': reason,
        'Permanent': False,
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/BanUsers', payload)
    if response and not response.get('200'):
        await ctx.send(f'Banned player {player_id} for {length} due to {reason}')
    else:
        await ctx.send('Failed to ban the player.')

@bot.command()
@commands.check(is_allowed_role)
async def deletemasterplayeraccount(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/DeleteMasterPlayerAccount', payload)
    if response and not response.get('200'):
        await ctx.send(f'Deleted master player account {player_id}')
    else:
        await ctx.send('Failed to delete master player account.')

@bot.command()
@commands.check(is_allowed_role)
async def searchforplayer(ctx, display_name):
    payload = {
        'TitleId': config["playfab_title_id"],
        'SearchTerm': display_name,
        'MatchFilter': 'DisplayName',
        'ReturnPlayFabId': True
    }
    response = make_playfab_request('Server/GetPlayersInSegment', payload, 'post')
    if response and response.get('200'):
        player_info = response.get('data', {}).get('PlayerProfiles', [])
        if player_info:
            player_ids = ', '.join([profile.get('PlayFabId') for profile in player_info])
            await ctx.send(f'Found player(s) with Display Name {display_name}: {player_ids}')
        else:
            await ctx.send(f'No player found with Display Name {display_name}')
    else:
        await ctx.send('Failed to search for the player.')

@bot.command()
@commands.check(is_allowed_role)
async def deletemasterplayer(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/DeleteMasterPlayer', payload)
    if response and not response.get('200'):
        await ctx.send(f'Deleted master player {player_id}')
    else:
        await ctx.send('Failed to delete master player.')

@bot.command()
@commands.check(is_allowed_role)
async def getuseraccountinfo(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/GetUserAccountInfo', payload)
    if response and not response.get('200'):
        user_account_info = response.get('data', {}).get('UserInfo', {})
        if user_account_info:
            account_info_message = f'User Account Info for {player_id}:\n{user_account_info}'
            await ctx.send(account_info_message)
        else:
            await ctx.send(f'No user account info found for {player_id}')
    else:
        await ctx.send('Failed to fetch user account info.')

@bot.command()
@commands.check(is_allowed_role)
async def getplayerprofile(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/GetPlayerProfile', payload)
    if response and not response.get('200'):
        player_profile = response.get('data', {}).get('PlayerProfile', {})
        if player_profile:
            profile_message = f'Player Profile for {player_id}:\n{player_profile}'
            await ctx.send(profile_message)
        else:
            await ctx.send(f'No player profile found for {player_id}')
    else:
        await ctx.send('Failed to fetch player profile.')

@bot.command()
@commands.check(is_allowed_role)
async def getuserbans(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/GetUserBans', payload)
    if response and not response.get('200'):
        user_bans = response.get('data', {}).get('Bans', [])
        if user_bans:
            bans_list = '\n'.join([f"Ban ID: {ban.get('BanId')} - Reason: {ban.get('BanReason')}" for ban in user_bans])
            bans_message = f'User Bans for {player_id}:\n{bans_list}'
            await ctx.send(bans_message)
        else:
            await ctx.send(f'No bans found for {player_id}')
    else:
        await ctx.send('Failed to fetch user bans.')

@bot.command()
@commands.check(is_allowed_role)
async def revokeban(ctx, ban_id):
    payload = {
        'BanId': ban_id
    }
    response = make_playfab_request('Admin/RevokeBan', payload)
    if response and not response.get('200'):
        await ctx.send(f'Revoked ban {ban_id}')
    else:
        await ctx.send('Failed to revoke ban.')

@bot.command()
@commands.check(is_allowed_role)
async def revokeallbans(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/RevokeAllBansForUser', payload)
    if response and not response.get('200'):
        await ctx.send(f'Revoked all bans for player {player_id}')
    else:
        await ctx.send('Failed to revoke all bans for the player.')

@bot.command()
@commands.check(is_allowed_role)
async def addcurrency(ctx, player_id, amount, currency):
    payload = {
        'PlayFabId': player_id,
        'VirtualCurrency': currency,
        'Amount': amount
    }
    response = make_playfab_request('Admin/AddUserVirtualCurrency', payload)
    if response and not response.get('200'):
        await ctx.send(f'Added {amount} {currency} to player {player_id}')
    else:
        await ctx.send('Failed to add currency.')

@bot.command()
@commands.check(is_allowed_role)
async def getuserinventory(ctx, player_id):
    payload = {
        'PlayFabId': player_id
    }
    response = make_playfab_request('Admin/GetUserInventory', payload)
    if response and not response.get('200'):
        user_inventory = response.get('data', {}).get('Inventory', [])
        if user_inventory:
            inventory_items = [f"Item: {item.get('DisplayName')} - Count: {item.get('RemainingUses')}" for item in user_inventory]
            inventory_chunks = [inventory_items[i:i + 10] for i in range(0, len(inventory_items), 10)]

            for chunk in inventory_chunks:
                inventory_message = f'User Inventory for {player_id}:\n' + '\n'.join(chunk)
                await ctx.send(inventory_message)
        else:
            await ctx.send(f'No inventory found for user {player_id}')
    else:
        await ctx.send('Failed to fetch user inventory.')

@bot.command()
@commands.check(is_allowed_role)
async def grantitem(ctx, player_id, item_id):
    payload = {
        'PlayFabId': player_id,
        'CatalogVersion': 'DLC',
        'ItemId': item_id
    }
    response = make_playfab_request('Admin/GrantItemsToUsers', payload)
    if response and not response.get('200'):
        await ctx.send(f'Granted item {item_id} to player {player_id}')
    else:
        await ctx.send('Failed to grant item.')

@bot.command()
@commands.check(is_allowed_role)
async def revokeitem(ctx, player_id, item_id):
    payload = {
        'PlayFabId': player_id,
        'ItemInstanceId': item_id
    }
    response = make_playfab_request('Admin/RevokeInventoryItem', payload)
    if response and not response.get('200'):
        await ctx.send(f'Revoked item {item_id} from player {player_id}')
    else:
        await ctx.send('Failed to revoke item.')

@bot.command()
@commands.check(is_allowed_role)
async def removecurrency(ctx, player_id, amount, currency):
    payload = {
        'PlayFabId': player_id,
        'VirtualCurrency': currency,
        'Amount': amount
    }
    response = make_playfab_request('Admin/SubtractUserVirtualCurrency', payload)
    if response and not response.get('200'):
        await ctx.send(f'Removed {amount} {currency} from player {player_id}')
    else:
        await ctx.send('Failed to remove currency.')

bot.run(config["discord_bot_token"])
