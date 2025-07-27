-- NetBox MySQL Database Setup
-- Run this script as root or a user with CREATE DATABASE privileges

-- Create the NetBox database
CREATE DATABASE IF NOT EXISTS netbox CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create NetBox user (adjust username/password as needed)
CREATE USER IF NOT EXISTS 'netbox'@'%' IDENTIFIED BY 'netbox123';

-- Grant privileges to NetBox user
GRANT ALL PRIVILEGES ON netbox.* TO 'netbox'@'%';

-- If you want to allow connections from localhost specifically
GRANT ALL PRIVILEGES ON netbox.* TO 'netbox'@'localhost';

-- Apply privileges
FLUSH PRIVILEGES;

-- Show the created database
SHOW DATABASES LIKE 'netbox';

-- Show the created user
SELECT User, Host FROM mysql.user WHERE User = 'netbox'; 