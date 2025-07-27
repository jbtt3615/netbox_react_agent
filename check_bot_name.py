#!/usr/bin/env python3
"""
Quick script to check bot name and info
"""

import configparser
from slack_bolt import App

def main():
    # Load config
    config = configparser.ConfigParser()
    config.read('resources/db_config.ini')
    
    bot_token = config.get('slack', 'SLACK_BOT_TOKEN')
    
    # Create app and test auth
    app = App(token=bot_token)
    
    try:
        auth_test = app.client.auth_test()
        print("🤖 Bot Information:")
        print(f"   Name: {auth_test['user']}")
        print(f"   User ID: {auth_test['user_id']}")
        print(f"   Team: {auth_test['team']}")
        print(f"   Team ID: {auth_test['team_id']}")
        print()
        print("💡 To invite the bot to a channel, use:")
        print(f"   /invite @{auth_test['user']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 