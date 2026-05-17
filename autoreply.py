from telethon import TelegramClient, events

api_id = 36022953
api_hash = 'd0da1904b3e98d0c784e7f7730c2cf23'

DEFAULT_REPLY = "Salom! Bu Avto Javob. Hozir band man, tez orada javob beraman."

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    await event.reply(DEFAULT_REPLY)

print("Auto-reply bot is running...")
client.start()
client.run_until_disconnected()