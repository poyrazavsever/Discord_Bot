from asyncio import tasks
from cgitb import reset
from dis import disco
from email import message
import discord
from discord.ext import commands, tasks
from utils import *
import time
import os 

intents = discord.Intents(messages =True, guilds = True, reactions = True, members = True, presences = True)
Bot = commands.Bot("!", intents = intents)

ext_file_types = ["png", "jpg", "jpeg", "gif" ]

ROOM = 0

roles = []
messages = []

@Bot.event
async def on_ready():
    await Bot.change_presence(activity= discord.Game(name = "Sizinle"))
    print("Bot çalışmaya başladı...")




@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels , name = "➠welcome")
    await channel.send(f"@{member} sunucumuza katıldı... Hoşgeldin!")



# @Bot.event
# async def on_message(message):
#     if len(message.attachments) > 0 and message.channel.name.startswith("➠questions"):
#         for ext in ext_file_types:
#             if message.attachments[0].filename.endswith(ext):
#                 await message.add_reaction("🇦")
#                 await message.add_reaction("🇧")
#                 await message.add_reaction("🇨")
#                 await message.add_reaction("🇩")
#                 await message.add_reaction("🇪")
#                 break


@Bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message in messages:
        for rs in roles:
            if rs[1] == str(reaction):
                await user.add_roles(rs[0])
    

class Social:
    INSTAGRAM = "https://instagram.com"
    TWITTER = "https://twitter.com"
    YOUTUBE = "https://youtube.com"


all_social_media = {
    'INSTAGRAM' : "p.avsever",
    'TWITTER' : "PoyrazAvsever",
    'YOUTUBE' : "PoyrazAvsever"
}

@Bot.command()
async def setSocial(ctx, s, absolute_path):
    """ s must be TWITTER, INSTAGRAM or YOUTUBE """
    all_social_media[s] = absolute_path
    print(all_social_media)


@Bot.command()
async def socialpush(ctx, room:discord.TextChannel):
    global ROOM 
    ROOM = room
    social_media_push.start()


@tasks.loop(seconds = 10)
async def social_media_push():
    await ROOM.send(getSocials())


def getSocials() ->str:
    return f"""
    
    {Social.YOUTUBE}/{all_social_media.get("YOUTUBE")}
    {Social.TWITTER}/{all_social_media.get("TWITTER")}
    {Social.INSTAGRAM}/{all_social_media.get("INSTAGRAM")}
    
    """

@Bot.command()
@commands.has_role("Staff-S")
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)
    
    await ctx.send("Mesajlar temizlendi!")
    time.sleep(4)
    await ctx.channel.purge(limit = 1)

@Bot.command()
async def socialpushstop(ctx):
    social_media_push.stop()



@Bot.command()
@commands.has_role("Staff-S")
async def clear_all(ctx):
    await ctx.channel.purge(limit = 1000)
    
    await ctx.send("Mesajların hepsi temizlendi!")
    time.sleep(4)
    await ctx.channel.purge(limit = 1)

@Bot.command()
@commands.has_role("Support Team")
async def kick(ctx, member : discord.Member, *args, reason = "Sebep Belirtilmedi..."):
    await ctx.send(f"{member} kullanıcısı kicklendi")
    await member.kick(reason = reason)




@Bot.command()
@commands.has_role("Support Team")
async def ban(ctx, member : discord.Member, *args, reason = "Sebep Belirtilmedi..."):
    await ctx.send(f"{member} kullanıcısı banlandı")
    await member.ban(reason = reason)




@Bot.command()
@commands.has_role("Support Team")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name , member_discriminator = member.split("#")

    #print(banned_users)
    #print(member_name)
    #print(member_id

    for bans in banned_users:
        user = bans.user

        if (user.name , user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} kullanıcısının banı açıldı.')
            return



@Bot.command()
async def load(ctx, extension):
    Bot.load_extension(f'cogs.{extension}')



@Bot.command()
async def unload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')
            

@Bot.command()
async def reload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')
    Bot.load_extension(f'cogs.{extension}')

    await ctx.send("Yenilendi...")
    

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        Bot.load_extension(f'cogs.{filename[:-3]}')



@Bot.command()
async def küfür(ctx):
    await ctx.message.add_reaction("🤬")

@Bot.command()
async def add_role(ctx, role: discord.Role, emoji:str, message_channel:str):
    channel_id , message_id = message_channel.split("/")[-2:]
    msg = await Bot.get_channel(int(channel_id)).fetch_message(int(message_id))

    await msg.add_reaction(emoji)
    messages.append(msg)


    for saved_roles in roles:
        if (role in saved_roles) or (emoji in saved_roles):
            await ctx.send("Bu rol veya emoji daha önceden kullanılmış. Lütfen başka bir rol veya emoji kullanınız.")
            return
            
    add_new_role(role, emoji)


def add_new_role(role,emoji):
    roles.append([role,emoji])
    print(roles)



Bot.run(TOKEN)
