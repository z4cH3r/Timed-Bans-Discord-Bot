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

embed_color = 0x0097FF   # Do not remove 0x  || Message Color. Hex, 6 characters. Do NOT include # | Helpful link https://htmlcolorcodes.com/color-picker/
embed_logo = "" #Direct Link to image. Leave blank to remove image.

server = discord.Server(id='450259793764941836') #Server ID. Needed for unban logic.
###################################################################################################################################################################

bot = commands.Bot(command_prefix=set_prefix)

@bot.event
async def on_ready():
    print("Bot connected!\nCurrently linked to {}".format(bot.user.name)) #Prints bots status and what bot token its connect to.
    await bot.change_presence(game=discord.Game(name="Timed ban system."))

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
            length_format = '{} Minutes(s)'.format(time)

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
        error = discord.Embed(colour=discord.Colour(embed_color), description="The ban time must be a **integer** not a **string**.")
        await bot.say(embed=error)

bot.run(bot_token)
