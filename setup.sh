#!/bin/bash

echo "🚀 NetBox React Agent + Slack Bot Setup"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your actual credentials before continuing!"
echo "   You'll need:"
echo "   - OpenAI API Key"
echo "   - Slack Bot Token"
echo "   - Slack Signing Secret"
echo "   - Slack App Token"
    echo ""
    echo "   After editing .env, run this script again."
    exit 0
fi

# Check if .env file has been configured
if grep -q "your-" .env; then
    echo "⚠️  Please configure your .env file with actual credentials before continuing!"
    echo "   Replace all 'your-*' values with your actual API keys and tokens."
    exit 1
fi

echo "✅ Environment variables configured"

# Create necessary directories
mkdir -p slack_bot

echo "🔧 Starting services..."
docker-compose up -d

echo ""
echo "🎉 Setup complete! Your services are starting up..."
echo ""
echo "📊 Service Status:"
echo "   - NetBox: http://localhost:8000 (admin/admin123)"
echo "   - Streamlit Agent: http://localhost:8501"
echo "   - Slack Bot: Running in background"
echo ""
echo "📋 Next Steps:"
echo "   1. Wait 2-3 minutes for all services to fully start"
echo "   2. Access NetBox at http://localhost:8000 (admin/admin123)"
echo "   3. Create an API token in NetBox (Admin > API Tokens)"
echo "   4. Update the NETBOX_TOKEN in your .env file"
echo "   5. Restart services: docker-compose restart"
echo ""
echo "💬 Slack Integration:"
echo "   - Add your bot to Slack channels"
echo "   - Mention the bot or send direct messages"
echo "   - Example: '@your-bot show me all devices'"
echo ""
echo "🔍 To view logs:"
echo "   docker-compose logs -f [service-name]"
echo "   (service names: postgres, redis, netbox, netbox_react_agent, slack_bot)" 