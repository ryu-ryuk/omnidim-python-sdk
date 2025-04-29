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


def main():
    omnidimension_client.call.dispatch_call(agent_id=912,to_number='+918160239777')

if __name__ == "__main__":
    main()