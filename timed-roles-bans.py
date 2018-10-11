import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import asyncio

###################################################################################################################################################################
#Config
bot_token = "" #Discord bot token. Find at https://discordapp.com/developers/applications/me
set_prefix = '!' #Sets command prefix.

public_logs = "491867518080909313" #Channel for Public ban logs.
private_logs = "491867537533829121" #Provides more detailed logs & unban system.
staff_role = "Staff" #Name of the role what is allowed to use this command. Must be completely correct, including capitalisation and spaces.

#Setting Role for chat & pug ban. Must be completely correct, including capitalisation and spaces.
chat_ban_role_set = 'Chat Ban'
custom_role_set = 'Pug Ban'
custom_tag = 'pug'
custom_formatted = 'Pug Ban'

embed_color = 0x0097FF   #Do not remove 0x  || Message Color. Hex, 6 characters. Do NOT include # | Helpful link https://htmlcolorcodes.com/color-picker/
embed_logo = "" #Direct Link to image. Leave blank to remove image.

server = discord.Server(id='450259793764941836') #Server ID. Needed for unban logic.
###################################################################################################################################################################

bot = commands.Bot(command_prefix=set_prefix)

banned_users = []

@bot.event
async def on_ready():
    print("Bot connected!\nCurrently linked to {}".format(bot.user.name)) #Prints bots status and what bot token its connect to.
    await bot.change_presence(game=discord.Game(name="Timed ban system."))

@bot.event
async def on_member_join(member):
    custom_role = discord.utils.get(member.server.roles, name=custom_role_set)
    chat_ban_role = discord.utils.get(member.server.roles, name=chat_ban_role_set)

    if member in banned_users:
        await bot.add_roles(member, custom_role, chat_ban_role)
        await bot.send_message(member, "Your account has been banned for 2 weeks\n This is due to leaving & rejoining the server with a active ban.")

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**User:** {}\n**Type:** Community\n**Reason:** Avoiding Bans\n**Length:** 2 Weeks".format(member))
        embed.set_thumbnail(url=embed_logo)
        await bot.send_message(bot.get_channel(public_logs),embed=embed)

        
        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** was just banned for **2 weeks**.\n**Reason:** Trying to avoid bans.".format(member))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

        await asyncio.sleep(1209600)
        await bot.remove_roles(member, custom_role, chat_ban_role)
        banned_users.remove(member)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** was just unbanned after **2 weeks**.".format(member))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

@bot.command(pass_context=True)
@commands.has_role(staff_role)
async def timedban(ctx, user, time, time_format, *reason):
    try:
        user = ctx.message.mentions[0]
        if time_format == 'weeks' or time_format == 'wks':
            length = int(time) * 604800
            length_format = '{} Week(s)'.format(time)
        elif time_format == 'hours' or time_format == 'hrs':
            length = int(time) / 0.00027777778
            length_format = '{} Hour(s)'.format(time)
        elif time_format == 'months' or time_format == 'mons':
            length = int(time) * 2629740
            length_format = '{} Month(s)'.format(time)
        elif time_format == 'minutes' or time_format == 'mins':
            length = int(time) / 0.016667
            length_format = '{} Minute(s)'.format(time)
        elif time_format == 'days' or time_format == 'ds':
            length = int(time) * 86400
            length_format = '{} Day(s)'.format(time)
        elif time_format == 'years' or time_format == 'yrs':
            length = int(time) * 31556952
            length_format = '{} Year(s)'.format(time)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**User:** {}\n**Type:** Server Ban\n**Reason:** {}\n**Length:** {}".format(user, ' '.join(reason), length_format))
        await bot.send_message(bot.get_channel(public_logs),embed=embed)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** banned **{}** for **{}**.".format(ctx.message.author, user, length_format))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

        await bot.ban(user, delete_message_days=0)
        await asyncio.sleep(length)
        await bot.unban(server, user)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** has been unbanned after **{}**.".format(user, length_format))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

    except:
        error = discord.Embed(colour=discord.Colour(embed_color), description="The ban time must be a **integer** not a **string**.\n or the command was entered incorrectly.")
        await bot.say(embed=error)

@bot.command(pass_context=True)
@commands.has_role(staff_role)
async def timedrole(ctx, user, ban_type, time, time_format, *reason):
    try:
        custom_role = discord.utils.get(ctx.message.server.roles,name=custom_role_set)
        chat_ban_role = discord.utils.get(ctx.message.server.roles,name=chat_ban_role_set)

        if ban_type == custom_tag:
            ban_type_formatted = custom_formatted
        elif ban_type == "community" or ban_type == "com":
            ban_type_formatted = "Community Ban"
        elif ban_type == "chat":
            ban_type_formatted = "Chat Ban"

        user = ctx.message.mentions[0]

        if time_format == 'weeks' or time_format == 'wks':
            length = int(time) * 604800
            length_format = '{} Week(s)'.format(time)
        elif time_format == 'hours' or time_format == 'hrs':
            length = int(time) / 0.00027777778
            length_format = '{} Hour(s)'.format(time)
        elif time_format == 'months' or time_format == 'mons':
            length = int(time) * 2629740
            length_format = '{} Month(s)'.format(time)
        elif time_format == 'minutes' or time_format == 'mins':
            length = int(time) / 0.016667
            length_format = '{} Minute(s)'.format(time)
        elif time_format == 'days' or time_format == 'ds':
            length = int(time) * 86400
            length_format = '{} Day(s)'.format(time)
        elif time_format == 'years' or time_format == 'yrs':
            length = int(time) * 31556952
            length_format = '{} Year(s)'.format(time)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**User:** {}\n**Type:** {} \n**Reason:** {}\n**Length:** {}".format(user, ban_type_formatted,' '.join(reason), length_format))
        await bot.send_message(bot.get_channel(public_logs),embed=embed)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** has given **{}** the role **{}** for **{}**.".format(ctx.message.author, user, ban_type_formatted, length_format))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)

        banned_users.append(user)

        if ban_type == custom_tag:
            await bot.add_roles(user, custom_role)
            await asyncio.sleep(length)
            await bot.remove_roles(user, custom_role)
            
        elif ban_type == "community" or ban_type == "com":
            await bot.add_roles(user, custom_role, chat_ban_role)
            await asyncio.sleep(length)
            await bot.remove_roles(user, custom_role, chat_ban_role)

        elif ban_type == "chat":
            await bot.add_roles(user, chat_ban_role)
            await asyncio.sleep(length)
            await bot.remove_roles(user, chat_ban_role)

        banned_users.remove(user)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="The role **{}** has been removed from **{}** after **{}**.".format(ban_type_formatted, user, length_format))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)
    
    except:
        error = discord.Embed(colour=discord.Colour(embed_color), description="The ban time must be a **integer** not a **string**.\n or the command was entered incorrectly.\nPlease note for the role system to work the discord bot must be above the role.")
        await bot.say(embed=error)

@bot.command(pass_context=True)
@commands.has_role(staff_role)
async def ban(ctx, user, *reason):
    try:
        user = ctx.message.mentions[0]
        await bot.ban(user, delete_message_days=0)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**User:** {}\n**Type:** Permanent Ban\n**Reason:** {}".format(user, ' '.join(reason)))
        await bot.send_message(bot.get_channel(public_logs),embed=embed)

        embed = discord.Embed(colour=discord.Colour(embed_color), description="**{}** banned **{}** **forever**.".format(ctx.message.author, user))
        await bot.send_message(bot.get_channel(private_logs),embed=embed)
    except:
        error = discord.Embed(colour=discord.Colour(embed_color), description="Unable to ban that user. This maybe due to incorrect formatting or the bot doesn't have permissions.")
        await bot.say(embed=error)        
        
bot.run(bot_token)
