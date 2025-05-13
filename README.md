# Omnidim SDK and MCP Server

A Python SDK for interacting with the Omnidim API, now with Model Context Protocol (MCP) server support.

## Installation

### Basic SDK

```bash
pip install omnidimension
```

### With MCP Server Support

```bash
pip install omnidimension[mcp]
```

## Usage

### SDK Usage

```python
from omnidimension import Client

# Initialize the client with your API key
client = Client(api_key="your_api_key")

# List agents
agents = client.agent.list()
print(agents)
```

### MCP Server Usage

You can run the MCP server in several ways:

1. Using the module:

```bash
python -m omnidimension.mcp_server --api-key your_api_key
```

2. Using the entry point:

```bash
omnidim-mcp-server --api-key your_api_key
```

3. Using the compatibility module (for MCP clients):

```bash
python -m omnidim_mcp_server --api-key your_api_key
```

You can also set the API key using the environment variable:

```bash
export OMNIDIM_API_KEY=your_api_key
python -m omnidimension.mcp_server
```

### MCP Client Configuration

To use with MCP clients like Claude Desktop, save the following configuration to `omnidim_mcp.json`:

```json
{
  "mcpServers": {
    "omnidim-mcp-server": {
      "command": "python3",
      "args": [
        "-m",
        "omnidim_mcp_server"
      ],
      "env": {
        "OMNIDIM_API_KEY": "<your_omnidim_api_key>"
      },
    }
  }
}
```