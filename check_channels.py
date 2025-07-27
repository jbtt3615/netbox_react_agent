#!/usr/bin/env python3
"""
Check which channels the bot is in
"""

import configparser
from slack_bolt import App

def main():
    # Load config
    config = configparser.ConfigParser()
    config.read('resources/db_config.ini')
    
    bot_token = config.get('slack', 'SLACK_BOT_TOKEN')
    
    # Create app
    app = App(token=bot_token)
    
    try:
        # Test auth first
        auth_test = app.client.auth_test()
        print(f"✅ Bot authenticated: {auth_test['user']}")
        
        # Get bot's conversations (channels)
        conversations = app.client.users_conversations(
            types="public_channel,private_channel,im,mpim"
        )
        
        if conversations['ok']:
            channels = conversations['channels']
            print(f"\n📋 Bot is in {len(channels)} conversation(s):")
            
            if not channels:
                print("   ❌ Bot is not in any channels yet")
                print("   💡 Try inviting it with: /invite @echo_bot")
            else:
                for channel in channels:
                    channel_type = channel['is_im'] and 'DM' or 'Channel'
                    channel_name = channel.get('name', f"DM with {channel.get('user', 'unknown')}")
                    print(f"   • {channel_type}: {channel_name}")
                    
        else:
            print(f"❌ Error getting conversations: {conversations['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 