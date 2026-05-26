import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

def search_youtube(query):
    ydl_opts = {"format": "bestaudio", "noplaylist": True, "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("ytsearch:" + query, download=False)
        return info["entries"][0]

@bot.command(name="p")
async def play(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("Join a voice channel first!")
    await ctx.send("Searching...")
    info = search_youtube(query)
    url = info["url"]
    title = info["title"]
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio(url))
    await ctx.send("Now playing: " + title)

@bot.command(name="stop")
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped!")

@bot.command(name="s")
async def skip(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Skipped!")

token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
