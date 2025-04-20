# (c) Evilxd
# A Part of MegaDL-Bot <https://github.com/codewithevilxd/MegaDL-Bot>

import os
import time
import ntplib
import asyncio
import datetime
from config import Config
from pyrogram import Client, idle
from pyrogram.session.internals import MsgId

# Force time synchronization with NTP server
def sync_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org', version=3)
        # Calculate the difference
        offset = response.offset
        print(f"Time offset: {offset} seconds")
        
        # Monkey patch the MsgId.get_new_msg_id function to use corrected time
        original_get_new_msg_id = MsgId.get_new_msg_id
        
        def patched_get_new_msg_id():
            # Add the offset to the current time to synchronize with server time
            return original_get_new_msg_id() + int(offset * 2**32)
        
        MsgId.get_new_msg_id = patched_get_new_msg_id
        
        return True
    except Exception as e:
        print(f"Time sync error: {e}")
        return False

if __name__ == "__main__" :
    # Try to sync time before starting the bot
    sync_successful = sync_time()
    if not sync_successful:
        print("Time sync failed, but continuing anyway...")
    
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="megadl")
    app = Client(
        "MegaDL-Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    app.start()
    print('\n\n>>> MegaDL-Bot Started. Join @codewithevilxd!')
    idle()
    app.stop()
    print('\n\n>>> MegaDL-Bot Stopped. Join @codewithevilxd!')
