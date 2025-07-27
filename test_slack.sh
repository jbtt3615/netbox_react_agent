#!/bin/bash

echo "🧪 Testing Slack Connection"
echo "==========================="

# Check if configuration file exists
if [ ! -f resources/db_config.ini ]; then
    echo "📝 Creating configuration file from template..."
    cp resources/db_config.ini.sample resources/db_config.ini
    echo ""
    echo "⚠️  IMPORTANT: Please edit resources/db_config.ini with your Slack credentials:"
    echo "   - SLACK_BOT_TOKEN (starts with xoxb-)"
    echo "   - SLACK_SIGNING_SECRET"
    echo "   - SLACK_APP_TOKEN (starts with xapp-)"
    echo ""
    echo "   Then run this script again."
    exit 0
fi

# Check if Slack credentials are configured
if grep -A 10 "\[slack\]" resources/db_config.ini | grep -q "your_"; then
    echo "⚠️  Please configure your resources/db_config.ini file with actual Slack credentials!"
    echo "   Replace all 'your_*' values with your actual Slack tokens."
    exit 1
fi

echo "✅ Configuration file ready"

# Check if Python dependencies are installed
echo "🔍 Checking Python dependencies..."
python3 -c "import slack_bolt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing Python dependencies. Installing..."
    pip3 install slack-bolt
fi

echo "✅ Dependencies ready"

# Test the connection
echo "🤖 Testing Slack connection..."
echo "   - This will verify your tokens are correct"
echo "   - The bot will respond to mentions and DMs"
echo "   - Press Ctrl+C to stop the test"
echo ""

python3 test_slack_connection.py 