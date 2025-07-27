# NetBox Slack Bot - Standalone Version

A standalone Slack bot that connects to your local MySQL database and uses OpenAI API for natural language processing. No web interface, no containers - just a simple Python script that runs locally.

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo>
cd netbox_react_agent
chmod +x run_bot.sh
./run_bot.sh
```

### 2. Configure Your Settings
Edit `resources/db_config.ini` with your actual credentials:
```ini
[mysql]
DB_HOST = localhost
DB_USER = root
DB_PASSWORD = Besp62sam
DB_PORT = 3306
DB_NAME = netbox

[netbox]
NETBOX_URL = http://localhost:8000
NETBOX_TOKEN = your_actual_netbox_token

[openai]
OPENAI_API_KEY = your_actual_openai_key

[slack]
SLACK_BOT_TOKEN = xoxb-your_actual_bot_token
SLACK_SIGNING_SECRET = your_actual_signing_secret
SLACK_APP_TOKEN = xapp-your_actual_app_token
```

### 3. Run the Bot
```bash
./run_bot.sh
```

## 📋 Prerequisites

- **Python 3.8+** installed
- **MySQL** running locally
- **NetBox** running (can be local or remote)
- **OpenAI API Key** (for GPT-4o)
- **Slack App** configured (see Slack Setup section)

## 🔧 Slack Setup

### 1. Create a Slack App
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name your app (e.g., "NetBox Assistant")
4. Select your workspace

### 2. Configure Bot Token Scopes
Go to "OAuth & Permissions" and add these scopes:
- `app_mentions:read`
- `channels:history`
- `chat:write`
- `im:history`
- `im:read`
- `im:write`

### 3. Enable Socket Mode
1. Go to "Socket Mode"
2. Enable Socket Mode
3. Create an app-level token (starts with `xapp-`)

### 4. Subscribe to Events
Go to "Event Subscriptions" and subscribe to:
- `app_mention`
- `message.im`

### 5. Install App
1. Go to "Install App"
2. Install to workspace
3. Copy the Bot User OAuth Token (starts with `xoxb-`)

### 6. Update Configuration
Add your Slack credentials to `resources/db_config.ini`

## 💬 Using the Bot

### Channel Mentions
```
@your-bot show me all devices
@your-bot create a new site called "DC2"
@your-bot what VLANs are in site DC1?
```

### Direct Messages
Send direct messages to the bot for private queries:
```
show me all IP addresses
delete device with ID 123
create a new VLAN with ID 100
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Local MySQL   │    │   NetBox API     │    │   OpenAI API    │
│   (Database)    │    │   (Remote/Local) │    │   (GPT-4o)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Standalone Bot │
                    │   (Python)      │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Slack API     │
                    │   (Socket Mode) │
                    └─────────────────┘
```

## 📊 Features

- ✅ **Standalone** - No containers, no web interface
- ✅ **Natural Language** - Chat with your network data
- ✅ **Slack Integration** - Access from anywhere via Slack
- ✅ **CRUD Operations** - Full Create, Read, Update, Delete
- ✅ **Local Database** - Uses your existing MySQL setup
- ✅ **Easy Setup** - One script to run everything

## 🛠️ Management

### Start the Bot
```bash
./run_bot.sh
```

### Stop the Bot
Press `Ctrl+C` in the terminal

### View Logs
Logs are displayed in the terminal where you run the bot

### Install Dependencies
```bash
pip3 install -r requirements_standalone.txt
```

## 🔍 Troubleshooting

### Bot Not Responding
1. Check that the bot is added to Slack channels
2. Verify bot token permissions
3. Ensure Socket Mode is enabled
4. Check the terminal logs for errors

### Configuration Errors
1. Verify `resources/db_config.ini` exists and is properly formatted
2. Check that all credentials are correct
3. Ensure no "your_*" placeholders remain

### Database Connection Issues
1. Verify MySQL is running
2. Check database credentials in config
3. Ensure the `netbox` database exists

### OpenAI API Errors
1. Verify API key is correct
2. Check API quota/limits
3. Ensure key has access to GPT-4o

## 📝 Example Queries

### Devices
```
"Show me all devices in DC1"
"List devices with status active"
"Get device details for router-01"
```

### Sites and Racks
```
"List all sites"
"Show racks in DC2"
"Create a new site called 'Branch Office'"
```

### IP Management
```
"Show all IP addresses"
"List IPs in subnet 192.168.1.0/24"
"Create IP address 192.168.1.100"
```

### VLANs
```
"List all VLANs"
"Show VLANs in site DC1"
"Create VLAN 100 with name 'Management'"
```

## 🔐 Security Notes

- Keep `resources/db_config.ini` secure (it's in `.gitignore`)
- Use strong API tokens
- Regularly update dependencies
- Monitor bot access and permissions

## 📦 Sharing the Setup

### For Team Members
1. Share the repository
2. Provide the `resources/db_config.ini.sample` template
3. Each person configures their own `resources/db_config.ini`
4. Run `./run_bot.sh`

### For Production
1. Use a process manager (systemd, supervisor)
2. Set up proper logging
3. Use environment variables for sensitive data
4. Configure monitoring and alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 