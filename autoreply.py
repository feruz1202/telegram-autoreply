from telethon import TelegramClient, events
import time

api_id = 36022953
api_hash = 'd0da1904b3e98d0c784e7f7730c2cf23'

DEFAULT_REPLY = "Salom! Bu Avto Javob. Hozir band man, tez orada javob beraman."

# Track last time YOU sent a message to each user
last_active = {}  # user_id: timestamp

COOLDOWN = 300  # 5 minutes - if you replied within 5 min, no auto-reply

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    sender = await event.get_sender()
    
    if sender.bot:
        return
    
    # Check if YOU were recently active with this person
    last_time = last_active.get(sender.id, 0)
    time_since_active = time.time() - last_time
    
    if time_since_active < COOLDOWN:
        print(f"You were active {int(time_since_active)}s ago, skipping auto-reply")
        return
    
    await event.reply(DEFAULT_REPLY)
    print(f"Auto-replied to {sender.username}")

@client.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
async def outgoing_handler(event):
    peer = await event.get_input_chat()
    entity = await client.get_entity(peer)
    last_active[entity.id] = time.time()
    print(f"You're active with {entity.id}, cooldown started")

print("Auto-reply bot is running...")
client.start()
client.run_until_disconnected()