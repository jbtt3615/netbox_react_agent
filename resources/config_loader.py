import os
import configparser
from typing import Dict, Any

class ConfigLoader:
    def __init__(self, config_path: str = "resources/db_config.ini"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from INI file"""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
    
    def get_mysql_config(self) -> Dict[str, str]:
        """Get MySQL configuration"""
        if 'mysql' not in self.config:
            raise KeyError("MySQL section not found in configuration")
        
        return {
            'DB_HOST': self.config.get('mysql', 'DB_HOST'),
            'DB_USER': self.config.get('mysql', 'DB_USER'),
            'DB_PASSWORD': self.config.get('mysql', 'DB_PASSWORD'),
            'DB_PORT': self.config.get('mysql', 'DB_PORT'),
            'DB_NAME': self.config.get('mysql', 'DB_NAME')
        }
    
    def get_netbox_config(self) -> Dict[str, str]:
        """Get NetBox configuration"""
        if 'netbox' not in self.config:
            raise KeyError("NetBox section not found in configuration")
        
        return {
            'NETBOX_URL': self.config.get('netbox', 'NETBOX_URL'),
            'NETBOX_TOKEN': self.config.get('netbox', 'NETBOX_TOKEN')
        }
    
    def get_openai_config(self) -> Dict[str, str]:
        """Get OpenAI configuration"""
        if 'openai' not in self.config:
            raise KeyError("OpenAI section not found in configuration")
        
        return {
            'OPENAI_API_KEY': self.config.get('openai', 'OPENAI_API_KEY')
        }
    
    def get_slack_config(self) -> Dict[str, str]:
        """Get Slack configuration"""
        if 'slack' not in self.config:
            raise KeyError("Slack section not found in configuration")
        
        return {
            'SLACK_BOT_TOKEN': self.config.get('slack', 'SLACK_BOT_TOKEN'),
            'SLACK_SIGNING_SECRET': self.config.get('slack', 'SLACK_SIGNING_SECRET'),
            'SLACK_APP_TOKEN': self.config.get('slack', 'SLACK_APP_TOKEN')
        }
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as a single dictionary"""
        config = {}
        config.update(self.get_mysql_config())
        config.update(self.get_netbox_config())
        config.update(self.get_openai_config())
        config.update(self.get_slack_config())
        return config
    
    def set_environment_variables(self):
        """Set all configuration values as environment variables"""
        all_config = self.get_all_config()
        for key, value in all_config.items():
            os.environ[key] = value
    
    def validate_config(self) -> bool:
        """Validate that all required configuration sections exist"""
        required_sections = ['mysql', 'netbox', 'openai', 'slack']
        for section in required_sections:
            if section not in self.config:
                print(f"❌ Missing required section: {section}")
                return False
        return True

def load_config() -> ConfigLoader:
    """Convenience function to load configuration"""
    return ConfigLoader()

def get_db_config() -> Dict[str, str]:
    """Get database configuration as a dictionary"""
    config = ConfigLoader()
    return config.get_mysql_config()

if __name__ == "__main__":
    # Test the configuration loader
    try:
        config = ConfigLoader()
        print("✅ Configuration loaded successfully")
        print(f"MySQL Host: {config.get_mysql_config()['DB_HOST']}")
        print(f"NetBox URL: {config.get_netbox_config()['NETBOX_URL']}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please ensure resources/db_config.ini exists and is properly formatted") 