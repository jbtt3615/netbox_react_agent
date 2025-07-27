#!/bin/bash

echo "🔧 Setting up MySQL Database for NetBox"
echo "======================================="

# Check if configuration file exists
if [ ! -f resources/db_config.ini ]; then
    echo "❌ Configuration file not found: resources/db_config.ini"
    echo "Please run ./start.sh first to create the configuration file."
    exit 1
fi

# Load configuration and set environment variables
echo "📝 Loading configuration..."
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

# Get database configuration from environment
DB_HOST=${DB_HOST:-localhost}
DB_USER=${DB_USER:-root}
DB_PASSWORD=${DB_PASSWORD}
DB_PORT=${DB_PORT:-3306}
DB_NAME=${DB_NAME:-netbox}

echo "🔍 Database Configuration:"
echo "   Host: $DB_HOST"
echo "   User: $DB_USER"
echo "   Port: $DB_PORT"
echo "   Database: $DB_NAME"

# Test MySQL connection
echo "🔍 Testing MySQL connection..."
if [ -z "$DB_PASSWORD" ]; then
    MYSQL_CMD="mysql -h $DB_HOST -P $DB_PORT -u $DB_USER"
else
    MYSQL_CMD="mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD"
fi

if ! $MYSQL_CMD -e "SELECT 1;" &> /dev/null; then
    echo "❌ Cannot connect to MySQL. Please check:"
    echo "   1. MySQL service is running"
    echo "   2. Credentials in resources/db_config.ini are correct"
    echo "   3. MySQL is accessible from this host"
    exit 1
fi

echo "✅ MySQL connection successful"

# Create database if it doesn't exist
echo "📝 Creating database '$DB_NAME' if it doesn't exist..."
$MYSQL_CMD -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if [ $? -eq 0 ]; then
    echo "✅ Database setup complete!"
    echo ""
    echo "📋 Database Details:"
    echo "   Database: $DB_NAME"
    echo "   User: $DB_USER"
    echo "   Host: $DB_HOST"
    echo "   Port: $DB_PORT"
    echo ""
    echo "🔧 You can now run ./start.sh to start the services"
else
    echo "❌ Database setup failed. Please check the error messages above."
    exit 1
fi 