# NetBox Slack Bot with OpenAI Integration

A powerful Slack bot that provides intelligent assistance for NetBox network infrastructure management using OpenAI's GPT models.

## 🚀 Features

- **🤖 AI-Powered Responses**: Uses OpenAI GPT-3.5-turbo for intelligent, contextual answers
- **📡 Slack Integration**: Works with direct messages and channel mentions
- **🔧 NetBox API Knowledge**: Comprehensive understanding of NetBox endpoints and operations
- **🔒 Secure Configuration**: API keys and credentials protected via `.gitignore`
- **🐳 Docker Ready**: Full containerization support for easy deployment
- **📊 MySQL Support**: Local database configuration for NetBox
- **🧪 Testing Tools**: Built-in connectivity and functionality tests

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Slack Workspace│    │  OpenAI API     │    │   NetBox API    │
│                 │    │                 │    │                 │
│ • Direct Messages│◄──►│ • GPT-3.5-turbo │    │ • Device Mgmt   │
│ • Channel Mentions│   │ • System Prompts│    │ • IP Management │
│ • Socket Mode    │    │ • Context Aware │    │ • Site Mgmt     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Standalone Bot │
                    │                 │
                    │ • Python 3.9+   │
                    │ • Slack Bolt    │
                    │ • LangChain     │
                    │ • MySQL Config  │
                    └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.9+**
- **MySQL** (local or containerized)
- **Slack App** with proper permissions
- **OpenAI API Key**
- **NetBox Instance** (optional for full functionality)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/jbtt3615/netbox_react_agent.git
cd netbox_react_agent
```

### 2. Set Up Configuration
```bash
# Copy the sample configuration
cp resources/db_config.ini.sample resources/db_config.ini

# Edit the configuration with your credentials
nano resources/db_config.ini
```

### 3. Install Dependencies
```bash
pip3 install -r requirements_standalone.txt
```

### 4. Test Slack Connection
```bash
./test_slack.sh
```

### 5. Start the Bot
```bash
python3 standalone_slack_bot.py
```

## 🔧 Configuration

Edit `resources/db_config.ini` with your credentials:

```ini
[mysql]
DB_HOST = localhost
DB_USER = root
DB_PASSWORD = your_actual_password
DB_PORT = 3306
DB_NAME = netbox

[netbox]
NETBOX_URL = http://netbox:8080
NETBOX_TOKEN = your_netbox_token_here

[openai]
OPENAI_API_KEY = sk-your_openai_api_key_here

[slack]
SLACK_BOT_TOKEN = xoxb-your_slack_bot_token_here
SLACK_SIGNING_SECRET = your_slack_signing_secret_here
SLACK_APP_TOKEN = xapp-your_slack_app_token_here
```

## 🛠️ Slack App Setup

### Required Bot Token Scopes:
- `app_mentions:read`
- `channels:join`
- `channels:read`
- `chat:write`
- `im:read`
- `im:write`
- `im:history`
- `channels:history`
- `groups:history`
- `mpim:history`
- `users:read`

### Required Events:
- `app_mention`
- `message`

### Required Socket Mode:
- Enable Socket Mode in your Slack app settings

See `SLACK_SETUP_GUIDE.md` for detailed setup instructions.

## 🧪 Testing

### Test Slack Connection
```bash
./test_slack.sh
```

### Test Bot Name
```bash
python3 check_bot_name.py
```

### Test Channel Status
```bash
python3 check_channels.py
```

## 🤖 Usage Examples

### Direct Messages
Send a direct message to your bot:
```
hello
what can you do?
how do I add a device to NetBox?
```

### Channel Mentions
Mention the bot in a channel:
```
@echo_bot how do I manage IP addresses?
@echo_bot show me the API for creating sites
```

### Sample Queries
- `"How do I add a new network device?"`
- `"What's the API call to list all IP addresses?"`
- `"Show me the JSON structure for creating a device"`
- `"How do I manage sites in NetBox?"`
- `"Explain NetBox device roles"`

## 🐳 Docker Deployment

### Full Containerized Setup
```bash
# Start all services (NetBox, MySQL, Redis, Bot)
docker-compose up -d
```

### Standalone Bot Only
```bash
# Build and run just the bot
docker build -f docker/Dockerfile -t netbox-slack-bot .
docker run --env-file .env netbox-slack-bot
```

## 📁 Project Structure

```
netbox_react_agent/
├── standalone_slack_bot.py      # Main bot application
├── resources/
│   ├── db_config.ini.sample     # Configuration template
│   ├── db_config.ini           # Your config (gitignored)
│   └── config_loader.py        # Configuration loader
├── test_slack_connection.py     # Slack connectivity test
├── test_slack.sh               # Test script
├── requirements_standalone.txt  # Python dependencies
├── docker-compose.yml          # Full stack deployment
├── docker/
│   └── Dockerfile              # Bot container
├── README_STANDALONE.md        # Detailed setup guide
├── SLACK_SETUP_GUIDE.md        # Slack app setup
└── .gitignore                  # Security protection
```

## 🔒 Security

- **API Keys**: Stored in `resources/db_config.ini` (gitignored)
- **Sample Files**: Only contain placeholder values
- **Environment Variables**: Supported for production deployment
- **SSL/TLS**: All API communications are encrypted

## 🚨 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'requests'"**
   ```bash
   pip3 install -r requirements_standalone.txt
   ```

2. **"invalid_auth" Slack Error**
   - Check your bot token in `resources/db_config.ini`
   - Ensure the app is installed to your workspace

3. **"missing_scope" Error**
   - Add required scopes in Slack app settings
   - Reinstall the app to your workspace

4. **OpenAI API Errors**
   - Verify your API key is correct
   - Check your OpenAI account balance

### Debug Mode
```bash
# Run with verbose logging
python3 standalone_slack_bot.py --debug
```

## 📚 Documentation

- **[README_STANDALONE.md](README_STANDALONE.md)** - Comprehensive setup guide
- **[SLACK_SETUP_GUIDE.md](SLACK_SETUP_GUIDE.md)** - Detailed Slack app configuration
- **[Docker Setup](docker-compose.yml)** - Containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NetBox** - Network infrastructure documentation
- **Slack** - Messaging platform and API
- **OpenAI** - AI language models
- **LangChain** - AI application framework

---

**Ready to deploy?** Follow the [Quick Start](#-quick-start) guide above to get your NetBox Slack bot running in minutes! 🚀
