# Samples for Semantic Kernel Chat Agent

This folder contains sample implementations demonstrating how to use the Semantic Kernel framework to create intelligent, context-aware chat agents. These examples showcase the integration of Azure OpenAI services and the creation of chat agents using the Semantic Kernel.

## Files in This Folder

### 1. **`sk-chat-agent.py`**
This script demonstrates how to:
- Initialize a Semantic Kernel instance.
- Add an Azure OpenAI Chat Completion service to the kernel.
- Create a `ChatCompletionAgent` for conversational interactions.
- Use the agent to generate responses to user queries.

### 2. **`sk-chat-agent-with-plugin.py`**
This script demonstrates how to:
- Create a custom plugin (SamplePlugin) with a simple function.
- Add the plugin to the Semantic Kernel.
- Use the plugin alongside a ChatCompletionAgent for enhanced functionality

### 3. **`sk-multi-agent.py`**
This script demonstrates how to:
- Create multiple ChatCompletionAgent instances with different instructions.
- Use the agents for specialized tasks, such as general queries and GitHub-related queries.

## Note

Before running the samples, ensure the environment creation is successful.

#### How to Run:
1. Ensure the `.env` file is properly configured.
2. Run the script using:
   ```bash
   python sk-chat-agent.py