from telethon import TelegramClient, events
import time

api_id = 36022953
api_hash = 'd0da1904b3e98d0c784e7f7730c2cf23'

DEFAULT_REPLY = "Salom! Hozir band man, tez orada javob beraman."

EXCLUDED_USERS = [
    "username1",
    "username2",
]

last_active = {}      # tracks when YOU last messaged someone
last_replied = {}     # tracks when bot last auto-replied to someone

COOLDOWN = 300        # 5 min - if you replied within 5 min, no auto-reply
REPLY_COOLDOWN = 300  # 5 min - if bot already replied, don't reply again until 5 min passes

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    sender = await event.get_sender()
    
    # Ignore bots
    if sender.bot:
        return
    
    # Ignore excluded users
    if sender.username in EXCLUDED_USERS:
        return
    
    # Check if YOU were recently active with this person
    last_time = last_active.get(sender.id, 0)
    if time.time() - last_time < COOLDOWN:
        return
    
    # Check if bot already replied to this person recently
    last_reply_time = last_replied.get(sender.id, 0)
    if time.time() - last_reply_time < REPLY_COOLDOWN:
        return
    
    await event.reply(DEFAULT_REPLY)
    last_replied[sender.id] = time.time()  # record when we replied
    print(f"Auto-replied to {sender.username}")

@client.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
async def outgoing_handler(event):
    peer = await event.get_input_chat()
    entity = await client.get_entity(peer)
    last_active[entity.id] = time.time()

print("Auto-reply bot is running...")
client.start()
client.run_until_disconnected()