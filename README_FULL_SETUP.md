# NetBox React Agent - Full Containerized Setup with Slack Integration

A complete containerized solution that includes NetBox, PostgreSQL, Redis, and an AI-powered React Agent accessible via both web interface and Slack.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Local MySQL   │    │      Redis       │    │     NetBox      │
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

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- MySQL server running locally
- OpenAI API Key
- Slack App credentials (see Slack Setup section)

### 1. Clone and Setup
```bash
git clone <your-repo>
cd netbox_react_agent
chmod +x setup.sh setup_mysql.sh
./setup_mysql.sh  # Set up MySQL database first
./setup.sh        # Then set up the services
```

### 2. Configure Environment
The setup script will create a `.env` file. Edit it with your credentials:

```bash
# MySQL Configuration (Local Database)
MYSQL_USER=netbox
MYSQL_PASSWORD=netbox123
MYSQL_PORT=3306

# NetBox Configuration
NETBOX_URL=http://netbox:8080
NETBOX_TOKEN=your-actual-netbox-token

# OpenAI Configuration
OPENAI_API_KEY=your-actual-openai-key

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
SLACK_SIGNING_SECRET=your-actual-signing-secret
SLACK_APP_TOKEN=xapp-your-actual-app-token
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Access Services
- **NetBox**: http://localhost:8000 (admin/admin123)
- **Streamlit Agent**: http://localhost:8501
- **Slack Bot**: Running in background

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

### 6. Update Environment
Add your Slack credentials to `.env`:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token
```

## 💬 Using the Slack Bot

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

## 🛠️ Service Management

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f netbox
docker-compose logs -f slack_bot
docker-compose logs -f netbox_react_agent
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
5. Restart services: `docker-compose restart`

## 🔍 Troubleshooting

### Services Not Starting
```bash
# Check service status
docker-compose ps

# Check logs for errors
docker-compose logs [service-name]
```

### Slack Bot Not Responding
1. Verify bot is added to channels
2. Check bot token permissions
3. Ensure Socket Mode is enabled
4. Check logs: `docker-compose logs slack_bot`

### NetBox Connection Issues
1. Wait for NetBox to fully start (2-3 minutes)
2. Verify API token is correct
3. Check NetBox logs: `docker-compose logs netbox`

### OpenAI API Errors
1. Verify API key is correct
2. Check API quota/limits
3. Ensure key has access to GPT-4o

## 📊 Service Ports

| Service | Port | Description |
|---------|------|-------------|
| NetBox | 8000 | Web interface |
| Streamlit | 8501 | Agent web interface |
| PostgreSQL | 5432 | Database (internal) |
| Redis | 6379 | Cache (internal) |

## 🔐 Security Notes

- Change default NetBox admin password
- Use strong API tokens
- Keep `.env` file secure
- Consider using Docker secrets in production
- Enable HTTPS in production

## 🚀 Production Deployment

For production use:
1. Use proper SSL certificates
2. Set up reverse proxy (nginx/traefik)
3. Use Docker secrets for sensitive data
4. Configure proper logging
5. Set up monitoring and alerts
6. Use external database for persistence

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 