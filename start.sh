#!/bin/bash

echo "🚀 Starting NetBox React Agent with Slack Integration"
echo "====================================================="

# Check if configuration file exists
if [ ! -f resources/db_config.ini ]; then
    echo "📝 Creating configuration file from template..."
    cp resources/db_config.ini.sample resources/db_config.ini
    echo ""
    echo "⚠️  IMPORTANT: Please edit resources/db_config.ini with your credentials:"
    echo "   - MySQL database settings"
    echo "   - OpenAI API Key"
    echo "   - Slack Bot credentials"
    echo ""
    echo "   Then run this script again."
    exit 0
fi

# Check if credentials are configured
if grep -q "your_" resources/db_config.ini; then
    echo "⚠️  Please configure your resources/db_config.ini file with actual credentials!"
    echo "   Replace all 'your_*' values with your actual credentials."
    exit 1
fi

echo "✅ Configuration file ready"

# Load configuration and set environment variables
echo "🔧 Loading configuration..."
python3 -c "
import sys
sys.path.append('resources')
from config_loader import ConfigLoader
config = ConfigLoader()
config.set_environment_variables()
print('✅ Configuration loaded successfully')
"

if [ $? -ne 0 ]; then
    echo "❌ Failed to load configuration. Please check resources/db_config.ini"
    exit 1
fi

# Start all services
echo "🔧 Starting services..."
docker-compose up -d

echo ""
echo "🎉 Services are starting up!"
echo ""
echo "📊 Service Status:"
echo "   - NetBox: http://localhost:8000 (admin/admin123)"
echo "   - Streamlit Agent: http://localhost:8501"
echo "   - Slack Bot: Running in background"
echo ""
echo "⏳ Please wait 2-3 minutes for all services to fully start"
echo ""
echo "🔍 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down" 