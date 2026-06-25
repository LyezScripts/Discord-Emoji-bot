import discord
from discord.ext import commands
import os
import re
import asyncio

TOKEN = "BOT_TOKEN"
GUILD_ID = GUILD_ID
EMOJI_FOLDER = "YOUR_NAME"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def format_emoji_name(name: str) -> str:
    name = re.sub(r'^\d+[-_\s]*', '', name)

    if "_" in name:
        parts = name.split("_")
        name = "_".join(p.capitalize() for p in parts if p)
    else:
        name = name.capitalize()

    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("Guild not found")
        await bot.close()
        return

    existing_names = {e.name.lower() for e in guild.emojis}

    for file in os.listdir(EMOJI_FOLDER):
        if not file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            continue

        raw_name = os.path.splitext(file)[0]
        emoji_name = format_emoji_name(raw_name)

        # handle duplicates
        base = emoji_name
        counter = 1

        while emoji_name.lower() in existing_names:
            emoji_name = f"{base}{counter}"
            counter += 1

        path = os.path.join(EMOJI_FOLDER, file)

        try:
            with open(path, "rb") as f:
                image = f.read()

            await guild.create_custom_emoji(
                name=emoji_name,
                image=image
            )

            existing_names.add(emoji_name.lower())
            print(f"Uploaded: {emoji_name}")

            # 🔥 RATE LIMIT (3 seconds)
            await asyncio.sleep(3)

        except discord.HTTPException as e:
            print(f"Failed {file}: {e}")
            await asyncio.sleep(3)

    print("Done uploading emojis.")
    await bot.close()

bot.run(TOKEN)
