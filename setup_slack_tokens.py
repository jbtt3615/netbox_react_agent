#!/usr/bin/env python3
"""
Slack Token Setup Helper
Guides you through getting your Slack tokens
"""

import os
import configparser

def main():
    print("🔑 Slack Token Setup Helper")
    print("=" * 40)
    print()
    
    print("📋 You need 3 tokens from Slack:")
    print("1. Bot User OAuth Token (xoxb-...)")
    print("2. Signing Secret")
    print("3. App-Level Token (xapp-...)")
    print()
    
    print("🚀 Let's get them step by step:")
    print()
    
    print("STEP 1: Create Slack App")
    print("- Go to https://api.slack.com/apps")
    print("- Click 'Create New App' → 'From scratch'")
    print("- Name: 'NetBox Assistant'")
    print("- Select your workspace")
    print("- Click 'Create App'")
    print()
    
    input("Press Enter when you've created the app...")
    
    print("STEP 2: Configure Bot Token Scopes")
    print("- Go to 'OAuth & Permissions' (left sidebar)")
    print("- Under 'Bot Token Scopes', add these scopes:")
    print("  • app_mentions:read")
    print("  • chat:write")
    print("  • im:read")
    print("  • im:write")
    print()
    
    input("Press Enter when you've added the scopes...")
    
    print("STEP 3: Enable Socket Mode")
    print("- Go to 'Socket Mode' (left sidebar)")
    print("- Toggle 'Enable Socket Mode' to ON")
    print("- Enter token name: 'netbox-bot-token'")
    print("- Click 'Generate App-Level Token'")
    print("- COPY the generated token (starts with xapp-)")
    print()
    
    app_token = input("Paste your App-Level Token (xapp-...): ").strip()
    
    print("STEP 4: Subscribe to Events")
    print("- Go to 'Event Subscriptions' (left sidebar)")
    print("- Toggle 'Enable Events' to ON")
    print("- Under 'Subscribe to bot events', add:")
    print("  • app_mention")
    print("  • message.im")
    print()
    
    input("Press Enter when you've subscribed to events...")
    
    print("STEP 5: Install App to Workspace")
    print("- Go to 'Install App' (left sidebar)")
    print("- Click 'Install to Workspace'")
    print("- Click 'Allow'")
    print("- COPY the 'Bot User OAuth Token' (starts with xoxb-)")
    print()
    
    bot_token = input("Paste your Bot User OAuth Token (xoxb-...): ").strip()
    
    print("STEP 6: Get Signing Secret")
    print("- Go to 'Basic Information' (left sidebar)")
    print("- Scroll to 'App Credentials'")
    print("- COPY the 'Signing Secret'")
    print()
    
    signing_secret = input("Paste your Signing Secret: ").strip()
    
    # Validate tokens
    if not bot_token.startswith('xoxb-'):
        print("❌ Bot token should start with 'xoxb-'")
        return
    
    if not app_token.startswith('xapp-'):
        print("❌ App token should start with 'xapp-'")
        return
    
    if not signing_secret:
        print("❌ Signing secret cannot be empty")
        return
    
    # Update config file
    config_path = "resources/db_config.ini"
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Update Slack section
    if 'slack' not in config:
        config['slack'] = {}
    
    config['slack']['SLACK_BOT_TOKEN'] = bot_token
    config['slack']['SLACK_SIGNING_SECRET'] = signing_secret
    config['slack']['SLACK_APP_TOKEN'] = app_token
    
    # Write back to file
    with open(config_path, 'w') as f:
        config.write(f)
    
    print("✅ Tokens saved to config file!")
    print()
    print("🎉 Setup complete! Now you can:")
    print("1. Run: ./test_slack.sh")
    print("2. Add bot to your channel: /invite @your-bot-name")
    print("3. Test with: @your-bot hello")
    print()

if __name__ == "__main__":
    main() 