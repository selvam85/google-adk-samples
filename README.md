# Google ADK Samples

A collection of examples demonstrating the [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) for building AI agents.

## Examples

| Example | Description | Blog Post |
|---------|-------------|-----------|
| [model_agnostic_agent](./model_agnostic_agent/) | Build agents that work with any LLM provider using LiteLLM | [Blog](https://selvamsubbiah.com/google-adk-litellm-model-agnostic-agents/) |
| [travel_agent](./travel_agent/) | Create custom tools including function tools and agents as tools | [Blog](https://selvamsubbiah.com/google-adk-custom-tools/) |

## Getting Started

1. Install dependencies:
   ```bash
   pip install google-adk python-dotenv
   ```

2. Set up your API keys in a `.env` file:
   ```bash
   GOOGLE_API_KEY=your_google_api_key
   ```

3. Run an example:
   ```bash
   adk run model_agnostic_agent
   # or
   adk run travel_agent
   ```

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Google ADK GitHub](https://github.com/google/adk-python)
