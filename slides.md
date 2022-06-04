---
author: Gabriel Antonio Videtta (@hearot)
paging: Diapositiva %d / %d
---

# Come pensare da zero un bot di Telegram con Python? Una guida passo dopo passo
Mi chiamo **Gabriel**, ma ormai sono più conosciuto con il mio
alias *hearot*. Ho diciotto anni e sono un grande amante della
matematica e della programmazione!

*Vivo* su Telegram ormai dal 2016 ed, avendone viste di cotte
e di crude, ho deciso di condividere con un ampio pubblico
tutto ciò che ho imparato riguardo alla programmazione di bot
tramite le API di Telegram.

---

# Prima di tutto, che cos'è un bot?
Citiamo senza indugio Wikipedia:

> Il **bot** [...] è un programma che accede alla rete attraverso lo stesso tipo di canali utilizzati dagli utenti [...]

Al di là della definizione tecnica (ed apparentemente banale), sono gli esempi che ci chiariscono immediatamente le idee:

> [...] (per esempio che accede alle pagine Web, invia messaggi in una chat, si muove nei videogiochi, e così via).

---

# Un bot: un utente programmato
Grazie a questi ultimi esempi, possiamo ridurre il bot alla
semplice definizione di **utente programmato**. Insomma, un bot è
semplicemente un programma che può accedere alle stesse funzioni
di un utente, automatizzandole nell'evenienza.

Ma è davvero così per Telegram?

---

# Userbot vs bot: quale dei due è un bot?
Rispondiamo velocemente alla domanda: **nì**.

Un bot, su Telegram, può rientrare nella definizione che abbiamo
presentato prima solo nel caso in cui, nell'effettivo, veniamo
riconosciuti dai server di Telegram come utenti.

Ciò vuol dire che dobbiamo predisporre di un numero di telefono e
che dobbiamo effettivamente creare un nuovo account di Telegram.

---

# Userbot vs bot, secondo la definizione classica
Nel caso di cui abbiamo appena discusso, staremmo parlando di
un cosiddetto *userbot*, un vero e proprio "utente-bot". Perché?
Perché risultiamo come utenti, anche se automatizzati, e come
tali accediamo alle medesime funzioni di un normalissimo
utente su Telegram.

E qui sorge il più grande dei dubbi: **creare un userbot è consentito?**

La risposta, fortunatamente, è sì, ed è proprio Telegram ad
elencare alcuni client più noti per raggiungere tale obiettivo su
https://telegram.org/apps.

---

# Userbot vs bot: due tipi di interazioni a confronto

Prima di tutto, chiariamo un concetto, ossia il modo in cui
bot e *userbot* interagiscono diversamente con i server di Telegram.

Mentre i bot usufruiscono delle **Bot API**, gli *userbot*
si connettono a Telegram con lo stesso protocollo impiegato
dai client degli utenti, ossia **MTProto**.

---

# Bot API, una semplice introduzione

Le **Bot API** sono API concesse e pubblicate ufficialmente
da Telegram per formalizzare e designare una piattaforma
mediante cui è possibile gestire i bot di Telegram stesso.

Lanciate per la prima volta nel Giugno 2015, esse hanno
ricevuto un aggiornamento significante nell'Aprile 2016
con l'introduzione di numerosi comandi.

---

# Bot API, come funzionano

In quanto API, esse hanno un endpoint (https://api.telegram.org)
ed un fattore di autenticazione (i.e. il token del bot, reperibile
tramite @BotFather) con il quale ci è possibile autenticarci.

Esse, tuttavia, non sono altro che MTProto! O meglio, ci
connettono ai server di Telegram, in un modo o nell'altro.

---

# Lo schema delle interazioni

Per intenderci, le **Bot API** ed i client di Telegram
giungono allo stesso fine, semplicemente con un passaggio
discriminante.

Bot API:

```
~~~graph-easy --as=boxart
[ Script ] - richiesta HTTP -> [ Bot API ] - richiesta MTProto -> [ Server di Telegram ]
~~~
```

Client MTProto:

```
~~~graph-easy --as=boxart
[ Script ] - richiesta MTProto -> [ Server di Telegram ]
~~~
```

---

# Vantaggi e svantaggi

Come abbiamo potuto notare dallo schema scorso, **i client MTProto
si connettono direttamente ai server di Telegram.**

Questo enorme vantaggio, che si riflette direttamente sulla velocità
di risposta di un bot, pone tuttavia talune limitazioni:

   - usare MTProto non permette di usare i cosiddetti *web hooks*,
     endpoint dei nostri server richiamati direttamente dalle Bot API
     non appena una nuova richiesta arriva ad un nostro bot;
   - le librerie che stiamo impiegando non sono più **ufficiali**.

---

# Il giusto compromesso: bot con MTProto

Ebbene, dal momento che i client MTProto non sono altro che
interagenti dei server Telegram, possiamo sfruttarli per
sviluppare bot, che sebbene distinti dagli *userbot*,
possano comunque evitare il traffico delle Bot API!

Insomma, connettersi a MTProto senza un numero di telefono,
il perfetto compromesso!

---

# Telethon, mettiamoci a lavoro

Per creare il nostro primo bot, installiamo Telethon,
una delle più rinomate librerie di Telegram:

```pip install telethon```

E scriviamo il nostro "hello world":

```
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

```

---

# API ID e API Hash

Per accedere ai server di Telegram, tuttavia, ci servono
tre parametri, che appositamente abbiamo lasciato incompleti
prima.

   - **API ID**
   - **API Hash**
   - **Bot Token**

Mentre i primi due sono ottenibili tramite https://my.telegram.org, il terzo, quello più personale, dobbiamo generarlo con @BotFather.

Una volta ottenuti, possiamo sostituirli nello script scorso prima.

---