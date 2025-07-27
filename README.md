# NetBox React Agent - Fully Containerized with Slack Integration

A complete containerized solution that includes NetBox, MySQL, Redis, and an AI-powered React Agent accessible via both web interface and Slack. Everything runs in Docker containers for easy sharing and deployment.

## 🚀 Quick Start (One Command)

```bash
# Clone the repository
git clone <your-repo>
cd netbox_react_agent

# Make startup script executable and run
chmod +x start.sh
./start.sh
```

The script will:
1. Create a `.env` file from template
2. Guide you through credential setup
3. Start all services automatically

## 📋 Prerequisites

- **Docker and Docker Compose** installed
- **OpenAI API Key** (for GPT-4o)
- **Slack App credentials** (see Slack Setup section)

## 🔧 Configuration

### 1. Environment Setup
Edit the `.env` file with your credentials:

```bash
# NetBox Configuration
NETBOX_URL=http://netbox:8080
NETBOX_TOKEN=your-netbox-api-token-here

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token-here
SLACK_SIGNING_SECRET=your-slack-signing-secret-here
SLACK_APP_TOKEN=xapp-your-slack-app-token-here
```

### 2. Slack App Setup
1. Go to https://api.slack.com/apps
2. Create a new app → "From scratch"
3. Configure bot token scopes:
   - `app_mentions:read`
   - `channels:history`
   - `chat:write`
   - `im:history`
   - `im:read`
   - `im:write`
4. Enable Socket Mode and create app-level token
5. Subscribe to events: `app_mention`, `message.im`
6. Install app to workspace
7. Copy tokens to `.env` file

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│     MySQL       │    │      Redis       │    │     NetBox      │
│   (Database)    │    │    (Caching)     │    │   (Web App)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Docker Network │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Streamlit Agent │    │   Slack Bot      │    │   Your Browser  │
│   (Port 8501)   │    │   (Background)   │    │   (Port 8000)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Services

| Service | Port | Description | Default Credentials |
|---------|------|-------------|-------------------|
| NetBox | 8000 | Web interface | admin/admin123 |
| Streamlit | 8501 | Agent web interface | - |
| MySQL | 3306 | Database | netbox/netbox123 |
| Redis | 6379 | Cache | - |

## 💬 Using the System

### Web Interface
- **NetBox**: http://localhost:8000
- **Streamlit Agent**: http://localhost:8501

### Slack Integration
- **Channel mentions**: `@your-bot show me all devices`
- **Direct messages**: Send private queries to the bot

### Example Queries
```
"Show me all devices in DC1"
"Create a new VLAN with ID 100"
"List all IP addresses"
"Delete device with ID 123"
```

## 🛠️ Management

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f netbox
docker-compose logs -f slack_bot
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart slack_bot
```

### Stop Services
```bash
docker-compose down
```

### Update NetBox Token
1. Access NetBox at http://localhost:8000
2. Go to Admin → API Tokens
3. Create a new token
4. Update `NETBOX_TOKEN` in `.env`
5. Restart: `docker-compose restart`

## 🔍 Troubleshooting

### Services Not Starting
```bash
# Check status
docker-compose ps

# Check logs
docker-compose logs [service-name]
```

### Slack Bot Issues
1. Verify bot is added to channels
2. Check bot token permissions
3. Ensure Socket Mode is enabled
4. Check logs: `docker-compose logs slack_bot`

### Database Issues
- MySQL data is persisted in Docker volume
- Reset database: `docker-compose down -v && docker-compose up -d`

## 📦 Sharing the Setup

### For Team Members
1. Share the repository
2. Provide the `.env.example` template
3. Each person runs `./start.sh`
4. Configure their own credentials

### For Production
1. Use proper SSL certificates
2. Set up reverse proxy
3. Use Docker secrets for sensitive data
4. Configure monitoring and backups
5. Use external database for persistence

## 🔐 Security Notes

- Change default NetBox admin password
- Use strong API tokens
- Keep `.env` file secure
- Enable HTTPS in production
- Regular security updates

## 📝 Features

- ✅ **Fully Containerized** - Everything runs in Docker
- ✅ **Natural Language Interface** - Chat with your network data
- ✅ **Slack Integration** - Access from anywhere via Slack
- ✅ **CRUD Operations** - Full Create, Read, Update, Delete
- ✅ **API Validation** - Ensures valid requests
- ✅ **Easy Sharing** - One command setup
- ✅ **Persistent Data** - MySQL data survives restarts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
