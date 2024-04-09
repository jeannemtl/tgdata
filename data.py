from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
import csv

######## ENTER PHONE NUMBER TO SIGN IN AS THIS +15148034148

# Your Telegram API credentials
api_id = '27277499'
api_hash = 'c87b9159de4d68651819afe97b289277'
# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def get_all_messages(channel_username):
    # Connect to Telegram
    await client.start()

    # Resolve the channel entity
    entity = await client.get_entity(channel_username)

    # Initialize an empty list to store all messages
    all_messages = []

    # Fetch messages in batches
    async for message in client.iter_messages(entity):
        all_messages.append(message)

    # Close the connection
    await client.disconnect()

    return all_messages


async def save_to_csv(messages, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Message ID', 'Date', 'Sender ID', 'Message'])
        for message in messages:
            writer.writerow([message.id, message.date, message.sender_id, message.text])

async def main():
    # Channel username (without '@')
    channel_username = 'jbean2021'
    
    # Get all messages from the channel
    all_messages = await get_all_messages(channel_username)

    # Save messages to CSV
    await save_to_csv(all_messages, 'messages.csv')

# Run the script
with client:
    client.loop.run_until_complete(main())