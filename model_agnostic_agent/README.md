# Model-Agnostic Agent

This example demonstrates how to build model-agnostic agents using Google ADK with LiteLLM integration. By using LiteLLM, you can switch between different LLM providers (Gemini, Claude, GPT, etc.) simply by changing an environment variable.

## Features

- Uses `LiteLlm` wrapper to support multiple LLM providers
- Configurable model via `LITELLM_MODEL` environment variable
- Includes sample tools: weather lookup and stock price checker

## Usage

Set the model via environment variable:

```bash
# Use Gemini (default)
export LITELLM_MODEL="gemini/gemini-3-flash-preview"

# Use Claude
export LITELLM_MODEL="anthropic/claude-sonnet-4-5-20250929"

# Use OpenAI
export LITELLM_MODEL="openai/gpt-5.2"
```

Run the agent:

```bash
adk run model_agnostic_agent
```

## Blog Post

For a detailed walkthrough, see the accompanying blog post:
[Google ADK + LiteLLM: Model-Agnostic Agents](https://selvamsubbiah.com/google-adk-litellm-model-agnostic-agents/)
