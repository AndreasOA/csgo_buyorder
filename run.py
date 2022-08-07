from src.get_current_skin_data import *
from datetime import datetime
import discord
import sys
import json
import pandas as pd

f = open("misc/credentials.json")
data = json.load(f)
f.close()
client = discord.Client()

TOKEN = data['discord_credentials']['token']
GUILD = int(data['discord_credentials']['guild'])
CHANNEL_ID = int(data['discord_credentials']['channel_id'])
SB_API_KEY = data['skinbaron_api_credentials']['api_key']
SLEEP_TIME_DEL = 15


@client.event
async def on_ready():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    sent_messages = []
    ai_f = open('misc/accepted_items.txt', 'r')
    accepted_items = ai_f.read().replace("'", "").split("\n")
    ai_f.close()
    split_f = open('misc/split_string.txt', 'r')
    eor_string = split_f.read()
    split_f.close()
    try:
        df_sb = pd.DataFrame()
        while True:
            print('Finding offers....')
            sent_messages, df_sb = await get_current_skin_data(SB_API_KEY, channel, sent_messages, df_sb, accepted_items, eor_string)
            print('offers found: ', len(sent_messages))


    except KeyboardInterrupt:
        sys.exit()
        
        

client.run(TOKEN)
