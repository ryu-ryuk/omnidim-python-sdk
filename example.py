import os
from omnidimension import Client

# Example usage of the Omnidimension SDK
api_key = os.environ.get('OMNIDIM_API_KEY', '3-rpvyQBbJiFutmR2Ak9CRQl7WmHTnwJJUBIPNQHVDY')
omnidimension_client = Client(api_key, base_url='http://localhost:8069/api/v1/')

def main_agent():
    # Get API key from environment variable or use a placeholder
    
    # Initialize the client
    
    # Example 1: List all agents
    print("\n=== Listing all agents ===")
    try:
        response = omnidimension_client.agent.list(page=1, page_size=10)
        print(f"Status: {response['status']}")
        print(f"Agents: {response['json']}")
    except Exception as e:
        print(f"Error listing agents: {e}")
    
    # Example 2: Create a prompt-based agent
    print("\n=== Creating a prompt-based agent ===")
    try:
        welcome_message = "Hello! I'm an example agent created using the Omnidimension SDK."
        context_breakdown = [
            {"title": "Purpose", "body": "This agent demonstrates the SDK capabilities."}
        ]
        
        response = omnidimension_client.agent.create(
            name="Example Agent",
            welcome_message="Hello! I'm an example agent created using the Omnidimension SDK.",
            context_breakdown=[
                {"title": "Purpose", "body": "This agent demonstrates the SDK capabilities."}
            ],
            transcriber={
                "provider": "deepgram_stream",
                # "model": "nova-3",
                # "language": "en-US",
                "silence_timeout_ms": 400   
            },
            model={
                # "provider": "openAI",
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                # "max_tokens": 150,
                # "top_p": 1,
                # "frequency_penalty": 0,
                # "presence_penalty": 0
            },
            voice={
                "provider": "eleven_labs",
                "voice_id": "JBFqnCBsd6RMkjVDRZzb"
            }, 
            web_search={
                "enabled": True, 
                "provider": "DuckDuckGo"
            },
            post_call_actions={
                "email": {
                    "enabled": True,
                    "recipients": ["example@example.com"],
                    "include": ["summary", "extracted_variables"]
                },
                "extracted_variables": [
                    {
                        "key": "caller_product_interest",
                        "prompt": "Identify the products the caller is interested in..."
                    },
                ]
            }
        )
        print(f"Status: {response['status']}")
        print(f"Created Agent: {response['json']}")
        
        # Store the agent ID for later examples
        agent_id = response['json'].get('id')
        if agent_id:
            # Example 3: Get agent details
            print("\n=== Getting agent details ===")
            response = omnidimension_client.agent.get(agent_id)
            print(f"Status: {response['status']}")
            print(f"Agent Details: {response['json']}")
            
            # Example 4: Update agent
            print("\n=== Updating agent ===")
            update_data =  {"name": "Updated Example Agent"}
            response = omnidimension_client.agent.update(agent_id, update_data)
            print(f"Status: {response['status']}")
            print(f"Updated Agent: {response['json']}")
            
            # Example 5: Delete agent
            # print("\n=== Deleting agent ===")
            # response = client.agent.delete(agent_id)
            # print(f"Status: {response['status']}")
            # print(f"Result: {response['json']}")
    
    except Exception as e:
        print(f"Error in agent operations: {e}")


def main_call_log():
    # omnidimension_client.call.dispatch_call(agent_id=912,to_number='+918160239777')
    result = omnidimension_client.call.get_call_logs()
    if len(result['json']['call_log_data']): 
        call_log_detail = omnidimension_client.call.get_call_log(
            call_log_id=result['json']['call_log_data'][0]['id']
        )
        print(call_log_detail['json'])
    else:
        print("No call logs found.")


def example_of_integrations():
    print("\n=== Integrations Examples ===")
    
    # Example 1: Get integration format examples
    print("\n--- Getting integration format examples ---")
    try:
        format_examples = omnidimension_client.integrations.get_integration_format_examples()
        print(f"Format Examples: {format_examples}")
    except Exception as e:
        print(f"Error getting format examples: {e}")
    
    # Example 2: Get user integrations
    print("\n--- Getting user integrations ---")
    try:
        response = omnidimension_client.integrations.get_user_integrations()
        print(f"Status: {response['status']}")
        print(f"User Integrations: {response['json']}")
    except Exception as e:
        print(f"Error getting user integrations: {e}")
    
    # Example 3: Create a custom API integration
    print("\n--- Creating a custom API integration ---")
    try:
        response = omnidimension_client.integrations.create_custom_api_integration(
            name="Weather API Integration",
            description="Integration with weather service",
            url="https://api.weatherapi.com/v1/current.json",
            method="GET",
            headers=[
                {"key": "Content-Type", "value": "application/json"}
            ],
            query_params=[
                {
                    "key": "key",
                    "description": "API Key for authentication",
                    "type": "string",
                    "required": True,
                    "isLLMGenerated": False
                },
                {
                    "key": "q",
                    "description": "Location query",
                    "type": "string",
                    "required": True,
                    "isLLMGenerated": True
                }
            ]
        )
        print(f"Status: {response['status']}")
        print(f"Created API Integration: {response['json']}")
        
        # Store the integration ID for later examples
        api_integration_id = response['json'].get('id')
    except Exception as e:
        print(f"Error creating custom API integration: {e}")
        api_integration_id = None
    
    # Example 4: Create a Cal.com integration
    print("\n--- Creating a Cal.com integration ---")
    try:
        response = omnidimension_client.integrations.create_cal_integration(
            name="Meeting Scheduler Integration",
            description="Integration with Cal.com calendar",
            cal_api_key="cal_api_key_example",
            cal_id="cal_user_id_example",
            cal_timezone="America/New_York"
        )
        print(f"Status: {response['status']}")
        print(f"Created Cal Integration: {response['json']}")
        
        # Store the integration ID for later examples
        cal_integration_id = response['json'].get('id')
    except Exception as e:
        print(f"Error creating Cal.com integration: {e}")
        cal_integration_id = None
    
    # Example 5: Create integration from JSON
    print("\n--- Creating integration from JSON ---")
    try:
        integration_data = {
            "name": "CRM API Integration",
            "description": "Integration with CRM service",
            "url": "https://api.crm-example.com/v1/contacts",
            "method": "POST",
            "integration_type": "custom_api",
            "headers": [
                {"key": "Authorization", "value": "Bearer token123"},
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body_type": "json",
            "body_params": [
                {
                    "key": "name",
                    "description": "Contact name",
                    "type": "string",
                    "required": True,
                    "isLLMGenerated": True
                },
                {
                    "key": "email",
                    "description": "Contact email",
                    "type": "string",
                    "required": True,
                    "isLLMGenerated": True
                },
                {
                    "key": "phone",
                    "description": "Contact phone number",
                    "type": "string",
                    "required": False,
                    "isLLMGenerated": True
                }
            ]
        }
        
        response = omnidimension_client.integrations.create_integration_from_json(integration_data)
        print(f"Status: {response['status']}")
        print(f"Created Integration from JSON: {response['json']}")
        
        # Store the integration ID for later examples
        json_integration_id = response['json'].get('id')
    except Exception as e:
        print(f"Error creating integration from JSON: {e}")
        json_integration_id = None
    
    # Example 6: Get agent integrations
    # First, create an agent to use for integration examples
    print("\n--- Creating an agent for integration examples ---")
    try:
        agent_response = omnidimension_client.agent.create(
            name="Integration Test Agent",
            welcome_message="Hello! I'm an agent for testing integrations.",
            context_breakdown=[
                {"title": "Purpose", "body": "This agent demonstrates integration capabilities."}
            ]
        )
        agent_id = agent_response['json'].get('id')
        
        if agent_id and api_integration_id:
            # Example 7: Add integration to agent
            print(f"\n--- Adding integration to agent (Agent ID: {agent_id}, Integration ID: {api_integration_id}) ---")
            try:
                response = omnidimension_client.integrations.add_integration_to_agent(
                    agent_id=agent_id,
                    integration_id=api_integration_id
                )
                print(f"Status: {response['status']}")
                print(f"Added Integration to Agent: {response['json']}")
            except Exception as e:
                print(f"Error adding integration to agent: {e}")
            
            # Example 8: Get agent integrations
            print(f"\n--- Getting agent integrations (Agent ID: {agent_id}) ---")
            try:
                response = omnidimension_client.integrations.get_agent_integrations(agent_id)
                print(f"Status: {response['status']}")
                print(f"Agent Integrations: {response['json']}")
            except Exception as e:
                print(f"Error getting agent integrations: {e}")
            
            # Example 9: Remove integration from agent
            print(f"\n--- Removing integration from agent (Agent ID: {agent_id}, Integration ID: {api_integration_id}) ---")
            try:
                response = omnidimension_client.integrations.remove_integration_from_agent(
                    agent_id=agent_id,
                    integration_id=api_integration_id
                )
                print(f"Status: {response['status']}")
                print(f"Removed Integration from Agent: {response['json']}")
            except Exception as e:
                print(f"Error removing integration from agent: {e}")
    except Exception as e:
        print(f"Error creating agent for integration examples: {e}")
    
    print("\n=== End of Integrations Examples ===")
    
if __name__ == "__main__":
    # Uncomment the function you want to run
    # main_agent()       # Run agent examples
    # main_call_log()    # Run call log examples
    example_of_integrations()  # Run integrations examples