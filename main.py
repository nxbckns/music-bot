import discord
from discord.ext import commands
import yt_dlp
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, format, *args):
        pass

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    server.serve_forever()

Thread(target=run_server, daemon=True).start()

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
    title
