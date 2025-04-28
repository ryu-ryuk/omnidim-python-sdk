import requests

class OmniClient:
    def __init__(self, api_key, base_url):
        """
        Initialize the OmniClient with API key and base URL.

        Args:
            api_key (str): The API key for authentication.
            base_url (str): The base URL of the API.
        """
        if not api_key or not base_url:
            raise ValueError("API key and base URL are required.")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def create_agent(self, agent_config, welcome_message, context_breakdown, **kwargs):
        """
        Create a custom agent with the provided configuration and optional parameters.

        Args:
            agent_config (dict): Configuration for the agent.
            welcome_message (str): Welcome message for the agent.
            context_breakdown (list): List of context breakdowns, each containing
                                      'title' and 'body'.
            **kwargs: Additional optional parameters to include in the API request.

        Returns:
            dict: Response from the API containing agent details.

        Raises:
            ValueError: If required fields are missing or invalid.
            requests.exceptions.RequestException: If the API request fails.
        """
        # Validate required inputs
        if not isinstance(agent_config, dict):
            raise ValueError("agent_config must be a dictionary.")
        if not isinstance(welcome_message, str):
            raise ValueError("welcome_message must be a string.")
        if not isinstance(context_breakdown, list) or not all(
            isinstance(context, dict) and 'title' in context and 'body' in context
            for context in context_breakdown
        ):
            raise ValueError(
                "context_breakdown must be a list of dictionaries with 'title' and 'body'."
            )

        # Prepare the API request
        url = f"{self.base_url}/agents/prompt-based"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        # Merge required fields with optional parameters
        data = {
            "agent_config": agent_config,
            "welcome_message": welcome_message,
            "context_breakdown": context_breakdown,
            **kwargs  # Include any additional parameters
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error and re-raise it
            print(f"Error creating agent: {e}")
            raise
