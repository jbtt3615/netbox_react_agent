#!/bin/bash

echo "🚀 Starting Standalone NetBox Slack Bot"
echo "======================================="

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

# Check if required files exist
if [ ! -f netbox_react_agent/netbox_apis.json ]; then
    echo "❌ Required file not found: netbox_react_agent/netbox_apis.json"
    exit 1
fi

# Check if Python dependencies are installed
echo "🔍 Checking Python dependencies..."
python3 -c "import slack_bolt, langchain_community, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing Python dependencies. Installing..."
    pip3 install slack-bolt langchain-community openai requests urllib3
fi

echo "✅ Dependencies ready"

# Start the bot
echo "🤖 Starting NetBox Slack Bot..."
echo "   - Press Ctrl+C to stop"
echo "   - Check logs for any errors"
echo ""

python3 standalone_slack_bot.py 