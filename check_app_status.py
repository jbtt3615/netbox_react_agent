#!/usr/bin/env python3
"""
Check app installation status and permissions
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
        # Test auth
        auth_test = app.client.auth_test()
        print("✅ Bot authentication successful!")
        print(f"   Bot name: {auth_test['user']}")
        print(f"   Team: {auth_test['team']}")
        
        # Check bot info
        bot_info = app.client.bots_info(bot=auth_test['user_id'])
        print(f"   Bot ID: {bot_info['bot']['id']}")
        print(f"   Bot name: {bot_info['bot']['name']}")
        
        # Check if bot is in any channels
        conversations = app.client.users_conversations(types="public_channel,private_channel")
        if conversations['channels']:
            print(f"   Bot is in {len(conversations['channels'])} channels")
            for channel in conversations['channels'][:3]:  # Show first 3
                print(f"     - {channel['name']}")
        else:
            print("   Bot is not in any channels yet")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 This might mean the app isn't properly installed to your workspace.")
        print("   Go to https://api.slack.com/apps → Your App → Install App → Install to Workspace")

if __name__ == "__main__":
    main() 