import discord
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

token = os.environ.get("DISCORD_TOKEN")
print(f"Token exists: {token is not None}")
client.run(token)
