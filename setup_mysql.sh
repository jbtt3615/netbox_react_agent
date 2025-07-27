#!/bin/bash

echo "🔧 MySQL Setup for NetBox"
echo "========================="

# Check if MySQL is running
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL client not found. Please install MySQL first."
    echo "   macOS: brew install mysql"
    echo "   Ubuntu: sudo apt-get install mysql-server"
    exit 1
fi

echo "✅ MySQL client found"

# Prompt for MySQL root password
read -s -p "Enter MySQL root password (or press Enter if no password): " MYSQL_ROOT_PASSWORD
echo ""

# Test MySQL connection
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    MYSQL_CMD="mysql -u root"
else
    MYSQL_CMD="mysql -u root -p$MYSQL_ROOT_PASSWORD"
fi

# Test connection
if ! $MYSQL_CMD -e "SELECT 1;" &> /dev/null; then
    echo "❌ Cannot connect to MySQL. Please check:"
    echo "   1. MySQL service is running"
    echo "   2. Root password is correct"
    echo "   3. MySQL is accessible"
    exit 1
fi

echo "✅ MySQL connection successful"

# Run the setup SQL
echo "📝 Setting up NetBox database..."
$MYSQL_CMD < mysql_setup.sql

if [ $? -eq 0 ]; then
    echo "✅ NetBox database setup complete!"
    echo ""
    echo "📋 Database Details:"
    echo "   Database: netbox"
    echo "   User: netbox"
    echo "   Password: netbox123"
    echo "   Host: localhost (or your MySQL host)"
    echo ""
    echo "🔧 You can now run ./setup.sh to start the services"
else
    echo "❌ Database setup failed. Please check the error messages above."
    exit 1
fi 