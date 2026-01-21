# Travel Agent

This example demonstrates how to create custom tools in Google ADK. It showcases function tools, built-in tools, and using agents as tools.

## Features

- **Custom Function Tools**: `get_flight_status` and `search_hotels` with typed parameters
- **Built-in Tools**: Uses `google_search` for web lookups
- **Agent as Tool**: Wraps a search agent using `AgentTool` so the main agent can delegate research tasks

## Tools Included

| Tool | Type | Description |
|------|------|-------------|
| `get_flight_status` | Function | Check flight status, gate, delays |
| `search_hotels` | Function | Search hotels in Paris, Tokyo, London |
| `web_search` | AgentTool | Sub-agent for web search using Google Search |

## Usage

```bash
adk run travel_agent
```

Example prompts:
- "What's the status of flight AA123?"
- "Find hotels in Paris for March 15-20, 2026"
- "What's the weather like in Tokyo?"

## Blog Post

For a detailed walkthrough, see the accompanying blog post:
[Google ADK: Custom Tools](https://selvamsubbiah.com/google-adk-custom-tools/)
