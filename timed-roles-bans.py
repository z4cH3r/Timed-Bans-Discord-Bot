import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import asyncio

###################################################################################################################################################################
#Config
bot_token = '' # Discord bot token. Find at https://discordapp.com/developers/applications/me
set_prefix = '!' # Sets command prefix.

public_logs = '' # Channel for Public ban logs.
private_logs = '' # Provides more detailed logs & unban system.
staff_role = 'Staff' # Name of the role what is allowed to use this command. Must be completely correct, including capitalisation and spaces.

#  Setting Role for chat & pug ban. Must be completely correct, including capitalisation and spaces.
chat_ban_role_set = 'Chat Ban'
custom_role_set = 'Pug Ban'
custom_tag = 'pug'
custom_formatted = 'Pug Ban'

embed_color = 0x0097FF   # Do not remove 0x  || Message Color. Hex, 6 characters. Do NOT include # | Helpful link https://htmlcolorcodes.com/color-picker/
###################################################################################################################################################################

bot = commands.Bot(command_prefix=set_prefix)

bans = {}

@bot.event
async def on_ready():
    print("Bot connected!\nCurrently linked to {}".format(bot.user.name))

@bot.event
async def on_member_join(member):
    custom_role = discord.utils.get(member.server.roles, name=custom_role_set)
    chat_ban_role = discord.utils.get(member.server.roles, name=chat_ban_role_set)
    perm_user = member.id
    if perm_user in bans:
        length = bans[perm_user] + 1209600
        bans.pop(perm_user)
        bans.update( {perm_user : length} )

        await bot.add_roles(member, custom_role, chat_ban_role)
        await bot.send_message(member, "Your account has been banned for an additional 2 weeks\nThis is due to leaving & rejoining the server with a active ban.")

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**User:** {}\n**Type:** Community\n**Reason:** Avoiding Bans\n**Length:** Original ban + 2 Weeks".format(member))
        await bot.send_message(bot.get_channel(public_logs),embed=embed)
        
        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** was just banned for an additional **2 weeks**.\n**Reason:** Trying to avoid bans.".format(member))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

        await asyncio.sleep(length)
        await bot.remove_roles(member, custom_role, chat_ban_role)
        bans.pop(perm_user)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** was just unbanned after **2 weeks** + his original ban.".format(member))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

@bot.command(pass_context=True)
@commands.has_role(staff_role)
async def timedrole(ctx, user, ban_type, time, time_format, *reason):
    custom_role = discord.utils.get(ctx.message.server.roles,name=custom_role_set)
    chat_ban_role = discord.utils.get(ctx.message.server.roles,name=chat_ban_role_set)

    if ban_type == custom_tag:
        ban_type_formatted = custom_formatted
    elif ban_type == "community" or ban_type == "com":
        ban_type_formatted = "Community Ban"
    elif ban_type == "chat":
        ban_type_formatted = "Chat Ban"

    user = ctx.message.mentions[0]
    perm_user = ctx.message.mentions[0].id

    if time_format == 'weeks' or time_format == 'wks' or time_format == 'week' or time_format == 'wk':
        length = int(time) * 604800
        length_format = '{} Week(s)'.format(time)
    elif time_format == 'hours' or time_format == 'hrs' or time_format == 'hour' or time_format == 'hr':
        length = int(time) / 0.00027777778
        length_format = '{} Hour(s)'.format(time)
    elif time_format == 'months' or time_format == 'mons' or time_format == 'month' or time_format == 'mon':
        length = int(time) * 2629740
        length_format = '{} Month(s)'.format(time)
    elif time_format == 'minutes' or time_format == 'mins' or time_format == 'minute' or time_format == 'min':
        length = int(time) / 0.016667
        length_format = '{} Minute(s)'.format(time)
    elif time_format == 'days' or time_format == 'ds' or time_format == 'day' or time_format == 'd':
        length = int(time) * 0.86400
        length_format = '{} Day(s)'.format(time)

    if perm_user in bans:
        ban_length = length + bans[perm_user]
        bans.pop(perm_user)
        bans.update( {perm_user : ban_length} )
    else:
        ban_length = length
        bans.update( {perm_user : length} )
        
    embed = discord.Embed(colour=discord.Colour(embed_color), description="**User:** {}\n**Type:** {} \n**Reason:** {}\n**Length:** {}".format(user, ban_type_formatted,' '.join(reason), length_format))
    await bot.send_message(bot.get_channel(public_logs),embed=embed)

    embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** has given **{}** the role **{}** for **{}**.".format(ctx.message.author, user, ban_type_formatted, length_format))
    await bot.send_message(bot.get_channel(private_logs),embed=embed)

    msg = 0

    if ban_type == custom_tag:
        await bot.add_roles(user, custom_role)
        await asyncio.sleep(ban_length)
        if ban_length >= bans[perm_user]:
            await bot.remove_roles(user, custom_role)
            bans.pop(perm_user)
            msg = 1

    elif ban_type == "community" or ban_type == "com":
        await bot.add_roles(user, custom_role, chat_ban_role)
        await asyncio.sleep(ban_length)
        if ban_length >= bans[perm_user]:
            await bot.remove_roles(user, custom_role, chat_ban_role)
            bans.pop(perm_user)
            msg = 1

    elif ban_type == "chat":
        await bot.add_roles(user, chat_ban_role)
        await asyncio.sleep(ban_length)
        if ban_length >= bans[perm_user]:
            await bot.remove_roles(user, chat_ban_role)
            bans.pop(perm_user)
            msg = 1

    if msg == 1:
        embed = discord.Embed(colour=discord.Colour(embed_color), description="The role **{}** has been removed from **{}** after **{}**.".format(ban_type_formatted, user, length_format))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

bot.run(bot_token)
