print# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Loading tg-script🚀")
import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import PeerChannel
import config  # Import the config file

# Start the Telegram client
client = TelegramClient(config.phone_number, config.api_id, config.api_hash)

async def fetch_members():
    await client.start()  # Connect to Telegram

    # Get the group by its username
    group = await client.get_entity(config.from_group_name)

    # Fetch all members of the group
    participants = await client.get_participants(group)

    # Print details of all members
    for participant in participants:
        print(f"ID: {participant.id}, Username: {participant.username}, Name: {participant.first_name} {participant.last_name}")

    # # Optionally, save the data to a file
    # with open('group_members.txt', 'w') as file:
    #     for participant in participants:
    #         file.write(f"ID: {participant.id}, Username: {participant.username}, Name: {participant.first_name} {participant.last_name}\n")

    # Open a CSV file for writing
    with open('group_members.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['ID', 'Username', 'First Name', 'Last Name'])

        # Write the details of each member to the CSV file
        for participant in participants:
            writer.writerow([
                participant.id, 
                participant.username, 
                participant.first_name, 
                participant.last_name
            ])

    # Print the total number of participants fetched
    print(f"Total participants fetched: {len(participants)}")
# Run the script
with client:
    client.loop.run_until_complete(fetch_members())
