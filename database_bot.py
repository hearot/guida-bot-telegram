import asyncio

from pymongo import MongoClient
from telethon import Button, TelegramClient, events, functions, types

from conf_primo_bot import admin_id, api_hash, api_id, bot_token

bot = TelegramClient("primo_bot", api_id, api_hash)
db = MongoClient().primo_bot

questionario = db.questionario
"""
questionario
============

user_id : int (id dell'utente)
nome : str (nome dell'utente)
gusto_preferito : str (gusto preferito dell'utente)
"""

tastiera = [
    [Button.inline("Compila questionario")],
    [Button.inline("Chiedi gelato")],
]

tastiera_admin = tastiera + [[Button.inline("Stampa questionari")]]


@bot.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    await event.respond("Ciao! Premi /menu.")


@bot.on(
    events.NewMessage(
        pattern="^/menu$",
    )
)
async def menu(event):
    if event.chat_id == admin_id:
        await event.respond(
            "Scegli un comando:",
            buttons=tastiera_admin,
        )
    else:
        await event.respond(
            "Scegli un comando:",
            buttons=tastiera,
        )


@bot.on(
    events.CallbackQuery(
        data="Stampa questionari", func=lambda e: e.chat_id == admin_id
    )
)
async def stampa_questionari(event):
    await event.delete()

    messaggio = "**Questionari:**\n\n"

    for questionario in db.questionario.find():
        messaggio += (
            " - " + questionario["nome"] + " - " + questionario["gusto_preferito"] + "\n"
        )

    await event.respond(messaggio)


@bot.on(events.CallbackQuery(data="Compila questionario"))
async def compila_questionario(event):
    await event.delete()

    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("Come ti chiami?")
        nome = (await conv.get_response()).text

        await conv.send_message("Qual è il tuo gusto preferito?")
        gusto_preferito = (await conv.get_response()).text.lower()

        await conv.send_message(
            f"Ciao {nome}, il tuo gusto preferito è il {gusto_preferito}!"
        )

        questionario.insert_one(
            {
                "user_id": event.chat_id,
                "nome": nome,
                "gusto_preferito": gusto_preferito,
            }
        )


@bot.on(events.CallbackQuery(data="Chiedi gelato"))
async def compila_questionario(event):
    await event.delete()

    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("Vorresti un cono o una coppetta?")

        while True:
            scelta = (await conv.get_response()).text.lower()

            if scelta in ["cono", "coppetta"]:
                break
            else:
                await conv.send_message(
                    "Risposta non valida. Vorresti un cono o una coppetta?"
                )

        await conv.send_message("Quale gusto vorresti?")
        gusto = (await conv.get_response()).text.lower()

        await conv.send_message(f"Ecco a te un gelato {scelta} e {gusto}!")

async def main():
    await bot.start(bot_token=bot_token)

    await bot(functions.bots.SetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code='',
            commands=[
                types.BotCommand(
                    command='start',
                    description='Avvia il bot'
                ),
                types.BotCommand(
                    command='menu',
                    description='Apri il menu del bot'
                )
            ]
    ))

    await bot.run_until_disconnected()


asyncio.run(main())
