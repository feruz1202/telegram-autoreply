from telethon import TelegramClient, events

api_id = 36022953
api_hash = 'd0da1904b3e98d0c784e7f7730c2cf23'

REPLIES = {
    "hello": "Salom, Bu Avto Javob",
    "hi": "Online bo'lishim bilanog javob beraman",
}

DEFAULT_REPLY = "Salom! Bu Avto Javob. Hozir band man, tez orada javob beraman."  # ← reply for ANY message

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    msg = event.message.text.lower()
    
    # Check keywords first
    for keyword, reply in REPLIES.items():
        if keyword in msg:
            await event.reply(reply)
            return
    
    # If no keyword matched, send default reply
    await event.reply(DEFAULT_REPLY)

print("Auto-reply bot is running...")
client.start()
client.run_until_disconnected()