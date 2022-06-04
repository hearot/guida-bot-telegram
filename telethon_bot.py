import asyncio

from telethon import TelegramClient, events

from conf_primo_bot import api_hash, api_id, bot_token

bot = TelegramClient("primo_bot", api_id, api_hash)


@bot.on(events.NewMessage())
async def handler(event):
    await event.respond("Ciao mondo!")


async def main():
    await bot.start(bot_token=bot_token)
    await bot.run_until_disconnected()


asyncio.run(main())
