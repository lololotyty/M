# (c) Evilxd
# A Part of MegaDL-Bot <https://github.com/codewithevilxd/MegaDL-Bot>

import os
import time
import socket
import struct
import asyncio
import datetime
from config import Config
from pyrogram import Client, idle
from pyrogram.session.internals import MsgId

# Force time synchronization without using ntplib
def sync_time():
    try:
        # NTP server
        NTP_SERVER = 'pool.ntp.org'
        # Reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800  # 1970-01-01 00:00:00
        
        # Connect to NTP server
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5.0)
        
        # NTP request packet (mode=3 for client)
        data = b'\x1b' + 47 * b'\0'
        
        # Send request
        client.sendto(data, (NTP_SERVER, 123))
        
        # Get response
        data, address = client.recvfrom(1024)
        
        # Check if response is valid (should be 48 bytes)
        if len(data) != 48:
            print("Invalid response from NTP server")
            return False
        
        # Extract timestamp (bytes 40-43 contain the server time)
        t = struct.unpack('!12I', data)[10]
        t -= TIME1970
        
        # Calculate the difference between local time and NTP time
        offset = t - time.time()
        
        print(f"Time offset: {offset} seconds")
        
        # Monkey patch the MsgId.get_new_msg_id function
        original_get_new_msg_id = MsgId.get_new_msg_id
        
        def patched_get_new_msg_id():
            # Use corrected time for generating message IDs
            return int((time.time() + offset) * 2**32)
        
        # Replace the original function
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
