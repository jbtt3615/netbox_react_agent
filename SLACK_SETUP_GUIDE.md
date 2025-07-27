# Slack Setup Guide

This guide will walk you through setting up Slack authentication for your NetBox bot.

## 🔑 What You Need

You'll need **3 tokens** from Slack:
1. **Bot User OAuth Token** (`xoxb-...`)
2. **Signing Secret** 
3. **App-Level Token** (`xapp-...`)

## 📋 Step-by-Step Setup

### 1. Create a Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter app name (e.g., "NetBox Assistant")
5. Select your workspace
6. Click **"Create App"**

### 2. Configure Bot Token Scopes

1. In your app, go to **"OAuth & Permissions"** (left sidebar)
2. Scroll down to **"Scopes"** section
3. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**
4. Add these scopes:
   - `app_mentions:read` - Read mentions of your bot
   - `channels:history` - Read channel messages
   - `chat:write` - Send messages
   - `im:history` - Read direct messages
   - `im:read` - Read direct message metadata
   - `im:write` - Send direct messages

### 3. Enable Socket Mode

1. Go to **"Socket Mode"** (left sidebar)
2. Toggle **"Enable Socket Mode"** to ON
3. Enter an app-level token name (e.g., "netbox-bot-token")
4. Click **"Generate App-Level Token"**
5. **Copy the generated token** (starts with `xapp-`)

### 4. Subscribe to Events

1. Go to **"Event Subscriptions"** (left sidebar)
2. Toggle **"Enable Events"** to ON
3. Under **"Subscribe to bot events"**, click **"Add Bot User Event"**
4. Add these events:
   - `app_mention` - When someone mentions your bot
   - `message.im` - When someone sends a direct message

### 5. Install App to Workspace

1. Go to **"Install App"** (left sidebar)
2. Click **"Install to Workspace"**
3. Review permissions and click **"Allow"**
4. **Copy the "Bot User OAuth Token"** (starts with `xoxb-`)

### 6. Get Signing Secret

1. Go to **"Basic Information"** (left sidebar)
2. Scroll down to **"App Credentials"**
3. **Copy the "Signing Secret"**

## 🔧 Configure Your Bot

### 1. Update Configuration File

Edit `resources/db_config.ini` with your tokens:

```ini
[slack]
SLACK_BOT_TOKEN = xoxb-your-actual-bot-token-here
SLACK_SIGNING_SECRET = your-actual-signing-secret-here
SLACK_APP_TOKEN = xapp-your-actual-app-token-here
```

### 2. Test the Connection

```bash
chmod +x test_slack.sh
./test_slack.sh
```

### 3. Add Bot to Channels

1. In Slack, go to a channel where you want the bot to work
2. Type `/invite @your-bot-name`
3. The bot will now respond to mentions in that channel

## 🧪 Testing Your Setup

### Test 1: Channel Mention
1. In a channel where the bot is added, type: `@your-bot hello`
2. The bot should respond with a test message

### Test 2: Direct Message
1. Click on your bot's name in Slack
2. Send a direct message: `hello`
3. The bot should respond

### Test 3: Check Logs
The terminal running the bot should show:
```
✅ Authentication successful!
   Bot User ID: U1234567890
   Bot Name: your-bot-name
   Team: Your Team Name
   Team ID: T1234567890
💬 Bot is ready to receive messages!
```

## 🔍 Troubleshooting

### "Authentication failed"
- Check that your Bot Token starts with `xoxb-`
- Verify the token is copied correctly (no extra spaces)
- Make sure the app is installed to your workspace

### "Socket Mode connection failed"
- Check that your App Token starts with `xapp-`
- Verify Socket Mode is enabled in your app settings
- Make sure the app-level token was generated

### "Bot not responding to mentions"
- Verify the bot is added to the channel (`/invite @bot-name`)
- Check that `app_mention` event is subscribed
- Ensure `app_mentions:read` scope is added

### "Bot not responding to DMs"
- Check that `message.im` event is subscribed
- Verify `im:read` and `im:write` scopes are added
- Make sure you're sending a direct message (not in a channel)

### "Permission denied"
- Check that all required scopes are added
- Verify the app is installed to your workspace
- Try reinstalling the app

## 📱 Bot Permissions Explained

- **`app_mentions:read`** - Bot can see when someone mentions it
- **`channels:history`** - Bot can read channel messages
- **`chat:write`** - Bot can send messages to channels
- **`im:history`** - Bot can read direct messages
- **`im:read`** - Bot can see direct message metadata
- **`im:write`** - Bot can send direct messages

## 🔐 Security Notes

- Keep your tokens secure and never share them
- The `resources/db_config.ini` file is in `.gitignore` for security
- Rotate tokens regularly in production
- Monitor bot usage and permissions

## ✅ Success Checklist

- [ ] App created in Slack
- [ ] Bot token scopes configured
- [ ] Socket Mode enabled
- [ ] Events subscribed
- [ ] App installed to workspace
- [ ] All 3 tokens copied to config file
- [ ] Test script runs successfully
- [ ] Bot responds to mentions
- [ ] Bot responds to DMs

Once you've completed this checklist, your Slack bot is ready to use! 🎉 