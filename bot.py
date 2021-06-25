
import os
from threading import Thread
import discord
from discord.ext import commands, tasks
from discord.utils import get
import requests
import time
import datetime
from dotenv import load_dotenv
import asyncio
import signal

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', description="I'm Donnie Foo", help_command=help_command, intents=intents)


@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('You\'re not in voice channel, join voice channel and run again')


@bot.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()


@bot.command()
async def hello(ctx):
  await ctx.send(ctx.author.mention + " hello!")

@bot.event
async def on_ready():
  print('Ready!')


async def on_member_join(member):
  print(f"{member} joined the server")


@bot.command(name="play")
async def play(ctx):
  print(ctx)
  # Gets voice channel of message author
  voice_channel = ctx.message.author.voice.channel
  channel = None
  if voice_channel != None:
      channel = voice_channel.name
      vc = await voice_channel.connect()
      vc.play(discord.FFmpegPCMAudio(source="/home/jrwhiteh/projects/donnie/media_va1VnYo.mp3"))
      # Sleep while audio is playing.
      while vc.is_playing():
          time.sleep(.1)
      await vc.disconnect()
  else:
      await ctx.send(str(ctx.author.name) + "is not in a channel.")
  # Delete command after the audio is done playing.
  await ctx.message.delete()

@bot.event
async def on_voice_state_update(member, prev, curr):
  print(member)
  if member.name == "gurgleswamp":
    if not curr.deaf:
      print('dudes listening')
      if curr.channel != None:
        print('in here')
        vc = await curr.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source="/home/jrwhiteh/projects/donnie/media_va1VnYo.mp3"))
        while vc.is_playing():
              time.sleep(.1)
        await vc.disconnect()


bot.run(TOKEN)
