#!/usr/bin/env python3
"""
Standalone NetBox Slack Bot
Connects to local MySQL and uses OpenAI API for natural language processing
"""

import os
import json
import logging
import requests
import difflib
import configparser
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import urllib3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    
    def get_mysql_config(self):
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
    
    def get_netbox_config(self):
        """Get NetBox configuration"""
        if 'netbox' not in self.config:
            raise KeyError("NetBox section not found in configuration")
        
        return {
            'NETBOX_URL': self.config.get('netbox', 'NETBOX_URL'),
            'NETBOX_TOKEN': self.config.get('netbox', 'NETBOX_TOKEN')
        }
    
    def get_openai_config(self):
        """Get OpenAI configuration"""
        if 'openai' not in self.config:
            raise KeyError("OpenAI section not found in configuration")
        
        return {
            'OPENAI_API_KEY': self.config.get('openai', 'OPENAI_API_KEY')
        }
    
    def get_slack_config(self):
        """Get Slack configuration"""
        if 'slack' not in self.config:
            raise KeyError("Slack section not found in configuration")
        
        return {
            'SLACK_BOT_TOKEN': self.config.get('slack', 'SLACK_BOT_TOKEN'),
            'SLACK_SIGNING_SECRET': self.config.get('slack', 'SLACK_SIGNING_SECRET'),
            'SLACK_APP_TOKEN': self.config.get('slack', 'SLACK_APP_TOKEN')
        }

class OpenAIClient:
    """Client for interacting with OpenAI API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = ChatOpenAI(
            openai_api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        logger.info("✅ OpenAI client initialized successfully")
    

    
    def send_message(self, message: str, system_prompt: str = "") -> str:
        """Send message to OpenAI and get response"""
        try:
            messages = []
            
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            
            messages.append(HumanMessage(content=message))
            
            response = self.client.invoke(messages)
            response_text = response.content
            
            logger.info(f"Received response from OpenAI: {response_text[:50]}...")
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to send message to OpenAI: {e}")
            return f"Error communicating with OpenAI: {str(e)}"
    
    def close(self):
        """Close OpenAI client (no cleanup needed)"""
        logger.info("Closed OpenAI client connection")

class NetBoxController:
    def __init__(self, netbox_url, api_token):
        self.netbox = netbox_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f"Token {self.api_token}",
        }

    def get_api(self, api_url: str, params: dict = None):
        response = requests.get(
            f"{self.netbox}{api_url}",
            headers=self.headers,
            params=params,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    def post_api(self, api_url: str, payload: dict):
        response = requests.post(
            f"{self.netbox}{api_url}",
            headers=self.headers,
            json=payload,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    def delete_api(self, api_url: str):
        response = requests.delete(
            f"{self.netbox}{api_url}",
            headers=self.headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()

class StandaloneNetBoxBot:
    def __init__(self):
        # Load configuration
        self.config = ConfigLoader()
        self.mysql_config = self.config.get_mysql_config()
        self.netbox_config = self.config.get_netbox_config()
        self.openai_config = self.config.get_openai_config()
        self.slack_config = self.config.get_slack_config()
        
        # Initialize components
        self.netbox_controller = NetBoxController(
            self.netbox_config['NETBOX_URL'],
            self.netbox_config['NETBOX_TOKEN']
        )
        
        # Initialize OpenAI client
        self.llm_client = OpenAIClient(self.openai_config['OPENAI_API_KEY'])
        
        # Initialize Slack app
        self.app = App(token=self.slack_config['SLACK_BOT_TOKEN'])
        
        # Set up Slack event handlers
        self.setup_slack_handlers()
    
    def process_with_llm(self, user_message: str, context: str = "") -> str:
        """Process user message with OpenAI"""
        try:
            # Create a comprehensive system prompt for the AI
            system_prompt = f"""You are an expert NetBox assistant with deep knowledge of network infrastructure management. You have access to NetBox APIs and can provide detailed guidance on network operations.

Context: {context}

## NETBOX API ENDPOINTS AVAILABLE:
- /api/dcim/devices/ - Network devices (routers, switches, servers)
- /api/dcim/sites/ - Physical locations and data centers
- /api/dcim/racks/ - Equipment racks and cabinets
- /api/ipam/ip-addresses/ - IP address management
- /api/ipam/aggregates/ - IP address aggregates/prefixes
- /api/ipam/asns/ - Autonomous System Numbers
- /api/dcim/cables/ - Physical cable connections
- /api/circuits/circuits/ - Network circuits and connections
- /api/virtualization/clusters/ - Virtual machine clusters
- /api/tenancy/contacts/ - Contact information
- /api/dcim/device-types/ - Device model templates
- /api/dcim/device-roles/ - Device function classifications

## COMMON API OPERATIONS:
- GET /api/dcim/devices/ - List all devices
- GET /api/dcim/devices/{id}/ - Get specific device details
- POST /api/dcim/devices/ - Create new device
- PUT /api/dcim/devices/{id}/ - Update device
- DELETE /api/dcim/devices/{id}/ - Delete device

## COMMON USE CASES:
1. **Device Management**: Add/remove/update network devices
2. **IP Address Management**: Assign/release IP addresses
3. **Site Management**: Organize devices by location
4. **Cable Management**: Track physical connections
5. **Circuit Management**: Manage network circuits
6. **Contact Management**: Store contact information

## RESPONSE GUIDELINES:
- Provide specific API endpoint examples when relevant
- Include sample JSON payloads for POST/PUT operations
- Explain the purpose and benefits of each operation
- Suggest best practices for network management
- Be concise but thorough in explanations

Please provide clear, actionable responses with specific API guidance when users ask about NetBox operations."""

            # Send to OpenAI
            response = self.llm_client.send_message(user_message, system_prompt)
            
            # Clean up the response
            response = response.strip()
            if not response:
                return "I'm sorry, I couldn't process your request. Please try again."
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing with OpenAI: {e}")
            return f"Sorry, I encountered an error processing your request: {str(e)}"

    def load_urls(self, file_path='netbox_react_agent/netbox_apis.json'):
        """Load supported URLs with their names from a JSON file"""
        if not os.path.exists(file_path):
            return {"error": f"URLs file '{file_path}' not found."}
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return [(entry['URL'], entry.get('Name', '')) for entry in data]
        except Exception as e:
            return {"error": f"Error loading URLs: {str(e)}"}

    def setup_slack_handlers(self):
        """Set up Slack event handlers"""
        
        @self.app.event("app_mention")
        def handle_mention(event, say):
            """Handle when the bot is mentioned in a channel"""
            user_message = event['text'].replace(f"<@{self.app.client.auth_test()['user_id']}>", "").strip()
            
            if not user_message:
                say("Hello! I'm your NetBox assistant. Ask me anything about your network infrastructure!")
                return
            
            self.process_message(user_message, say)

        @self.app.event("message")
        def handle_dm(event, say):
            """Handle direct messages to the bot"""
            if event.get('channel_type') == 'im':
                user_message = event['text'].strip()
                
                if not user_message:
                    say("Hello! I'm your NetBox assistant. Ask me anything about your network infrastructure!")
                    return
                
                self.process_message(user_message, say)

    def process_message(self, user_message, say):
        """Process user message and respond"""
        try:
            logger.info(f"Processing message: {user_message}")
            
            # Get available APIs for context
            apis = self.load_urls()
            if not isinstance(apis, dict):
                api_list = [f"{name} ({url})" for url, name in apis[:10]]  # Show first 10 APIs
                context = f"Available NetBox APIs ({len(apis)} total): {', '.join(api_list)}"
            else:
                context = "Error loading APIs - using default NetBox knowledge"
            
            # Process with private LLM
            response = self.process_with_llm(user_message, context)
            
            # Format the response for Slack
            formatted_response = self.format_response_for_slack(response)
            say(formatted_response)
            
            logger.info("Response sent successfully")
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            say(error_msg)
            logger.error(f"Error processing message: {e}")

    def format_response_for_slack(self, response_text):
        """Format the response for Slack display"""
        # For regular text responses
        if len(response_text) > 3000:
            return response_text[:3000] + "\n\n... (response truncated)"
        
        return response_text

    def run(self):
        """Start the Slack bot"""
        logger.info("🚀 Starting NetBox Slack Bot with OpenAI...")
        logger.info(f"📊 MySQL Host: {self.mysql_config['DB_HOST']}")
        logger.info(f"🔗 NetBox URL: {self.netbox_config['NETBOX_URL']}")
        logger.info("🤖 OpenAI API: Configured")
        logger.info("💬 Bot is ready to receive messages!")
        
        try:
            # Start the Slack bot
            handler = SocketModeHandler(self.app, self.slack_config['SLACK_APP_TOKEN'])
            handler.start()
        finally:
            # Clean up LLM client
            self.llm_client.close()

def main():
    """Main entry point"""
    try:
        bot = StandaloneNetBoxBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot failed to start: {e}")
        raise

if __name__ == "__main__":
    main() 