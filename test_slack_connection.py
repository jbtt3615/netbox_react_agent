#!/usr/bin/env python3
"""
Simple Slack Connection Test
Tests basic Slack authentication and connection
"""

import os
import logging
import configparser
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    
    def get_slack_config(self):
        """Get Slack configuration"""
        if 'slack' not in self.config:
            raise KeyError("Slack section not found in configuration")
        
        return {
            'SLACK_BOT_TOKEN': self.config.get('slack', 'SLACK_BOT_TOKEN'),
            'SLACK_SIGNING_SECRET': self.config.get('slack', 'SLACK_SIGNING_SECRET'),
            'SLACK_APP_TOKEN': self.config.get('slack', 'SLACK_APP_TOKEN')
        }

class SimpleSlackBot:
    def __init__(self):
        # Load configuration
        self.config = ConfigLoader()
        self.slack_config = self.config.get_slack_config()
        
        # Initialize Slack app
        self.app = App(token=self.slack_config['SLACK_BOT_TOKEN'])
        
        # Set up basic event handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up basic Slack event handlers"""
        
        @self.app.event("app_mention")
        def handle_mention(event, say):
            """Handle when the bot is mentioned in a channel"""
            user_message = event['text'].replace(f"<@{self.app.client.auth_test()['user_id']}>", "").strip()
            
            if not user_message:
                say("Hello! I'm your NetBox assistant. This is a test connection - I'm working! 🤖")
                return
            
            say(f"Test response: I received your message: '{user_message}'. Connection is working! ✅")

        @self.app.event("message")
        def handle_dm(event, say):
            """Handle direct messages to the bot"""
            if event.get('channel_type') == 'im':
                user_message = event['text'].strip()
                
                if not user_message:
                    say("Hello! I'm your NetBox assistant. This is a test connection - I'm working! 🤖")
                    return
                
                say(f"Test response: I received your message: '{user_message}'. Connection is working! ✅")

        @self.app.event("app_home_opened")
        def handle_app_home_opened(event, say):
            """Handle when someone opens the app home"""
            logger.info(f"App home opened by user: {event['user']}")

    def test_connection(self):
        """Test the Slack connection"""
        try:
            # Test auth
            auth_test = self.app.client.auth_test()
            logger.info(f"✅ Authentication successful!")
            logger.info(f"   Bot User ID: {auth_test['user_id']}")
            logger.info(f"   Bot Name: {auth_test['user']}")
            logger.info(f"   Team: {auth_test['team']}")
            logger.info(f"   Team ID: {auth_test['team_id']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            return False

    def run(self):
        """Start the Slack bot"""
        logger.info("🚀 Starting Simple Slack Bot Test...")
        
        # Test connection first
        if not self.test_connection():
            logger.error("❌ Cannot start bot - authentication failed")
            return
        
        logger.info("💬 Bot is ready to receive messages!")
        logger.info("   - Mention the bot in a channel: @your-bot hello")
        logger.info("   - Send a direct message to the bot")
        logger.info("   - Press Ctrl+C to stop")
        
        try:
            # Start the Slack bot
            handler = SocketModeHandler(self.app, self.slack_config['SLACK_APP_TOKEN'])
            handler.start()
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Bot failed: {e}")
            raise

def main():
    """Main entry point"""
    try:
        bot = SimpleSlackBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main() 