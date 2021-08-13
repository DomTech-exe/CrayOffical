import discord
import os
from discord.ext import commands
from discord import guild
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members=True

bot = commands.Bot(intents=intents, command_prefix='.')
bot.remove_command('help')

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('.help'))
  print ("Cray is ready!")



@bot.command()
async def hello(ctx, *, args = None):
    await ctx.send('hello')

@bot.command()
async def ping(ctx, *, args = None):
    await ctx.send('Pong!')


@bot.command()
async def say(ctx, arg):
  await ctx.send(arg)
  
@bot.command()
async def server(ctx):
  name = ctx.guild.name
  

  memberCount = ctx.guild.member_count

  
  embed = discord.Embed(
    title=name + " Server Information ",
    
    
  )
  
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)



@bot.command()
async def help(ctx):
  name = "Commands Help Manual"
  

  helpCommand = "This command is used to see the commannds manual "

  pingCommand = "This command is used to see if the bot is online "

  kickCommand = "This commands kicks a member from the Discord Server"
  
  banCommand = "This commands bans a member from the Discord Server"

  sayCommand = "This command makes Cray say whatever you want. Example: .say Hey there!"

  muteCommand = "This command mutes a member in a Discord Server"

  unmuteCommand = "This command unmutes a member in a Discord Server"


  embed = discord.Embed(
    title=name 
    
    
  )
  
  embed.add_field(name=".help", value=helpCommand, inline=False)


  embed.add_field(name=".ping", value=pingCommand, inline=False)

  embed.add_field(name=".say", value=sayCommand, inline=False)

  embed.add_field(name=".kick", value=kickCommand, inline=False)

  embed.add_field(name=".ban", value=banCommand, inline=False)

  embed.add_field(name=".mute", value=muteCommand, inline=False)

  embed.add_field(name=".unmute", value=unmuteCommand, inline=False)
 
  await ctx.send(embed=embed)

@bot.event 
async def on_member_join(member):
  print(f'{member} has joined the server!')

  embed=discord.Embed(title=f"{member.name} has joined the server!",
  description=f"Member #{len(list(member.guild.members))}")
  embed.set_thumbnail(url=f"{member.avatar_url}")
  channel = bot.get_channel(id=871386007323430973)
  await channel.send(embed=embed)

@bot.event 
async def on_member_remove(member):
  print(f'{member} has left the server!')

  embed=discord.Embed(title=f"{member.name} has left the server!",
  description=f"Wish that they had a great time!")
  embed.set_thumbnail(url=f"{member.avatar_url}")
  channel = bot.get_channel(id=871386007323430973)
  await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send (f'I have kicked {member} succesfully!')


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'I have banned {member} successfully!')



@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" You have been muted from: {guild.name} reason: {reason}")



@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

  await member.remove_roles(mutedRole)
  await member.send(f" You have been unmuted from: - {ctx.guild.name}")
  embed = discord.Embed(title="unmute", description=f" Unmuted-{member.mention}",colour=discord.Colour.light_gray())
  await ctx.send(embed=embed)



keep_alive()
bot.run(os.getenv('TOKEN'))
