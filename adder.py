import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
import config  # Import the config file
import time

# Start the Telegram client using values from the config file
client = TelegramClient(config.phone_number, config.api_id, config.api_hash)
import config

MAX_INVITES_PER_DAY = 50  # Set your daily limit
invite_count = 0  # Counter for the number of users added

async def add_members_to_group():
    await client.start()  # Connect to Telegram

    # Get the target group entity by its username
    target_group = await client.get_entity(config.to_group_name)

    # Read members from the CSV file
    with open('group_members.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if invite_count >= MAX_INVITES_PER_DAY:
                print(f"Reached the maximum of {MAX_INVITES_PER_DAY} invites for today.")
                break
            try:
                # Get the user by their ID or username
                if row['Username']:
                    user = await client.get_entity(row['Username'])  # Invite by username
                else:
                    user = await client.get_entity(int(row['ID']))  # Invite by ID if no username

                # Add the user to the target group
                await client(InviteToChannelRequest(
                    target_group,  # The target group
                    [user]  # The user to be added
                ))

                print(f"Successfully added {row['Username'] or row['ID']} to the group")
                invite_count += 1  # Increment the invite counter

                # Introduce a delay to avoid hitting the rate limit
                time.sleep(10)  # Add a 10-second delay between each invite
            
            except Exception as e:
                print(f"Failed to add {row['Username'] or row['ID']} to the group: {e}")
                if 'wait' in str(e).lower():
                    wait_time = int(''.join(filter(str.isdigit, str(e))))  # Extract the wait time from the error message
                    print(f"Waiting for {wait_time} seconds due to rate limit.")
                    time.sleep(wait_time)  # Wait for the required time before continuing


    print("Finished adding members.")

# Run the script
with client:
    client.loop.run_until_complete(add_members_to_group())
