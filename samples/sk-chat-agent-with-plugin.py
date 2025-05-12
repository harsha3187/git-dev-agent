from semantic_kernel import Kernel
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from dotenv import load_dotenv
import os

if os.path.exists(".env"):
    load_dotenv(override=True)
else:
    # Load environment variables from the parent 
    current_dir = os.getcwd()
    env_path = os.path.join(current_dir, '..', '.env')
    load_dotenv(dotenv_path=env_path)

# Define a Sample Plugin
class SamplePlugin:
    @kernel_function
    async def greet(self, name: str) -> str:
        return f"Hello, {name}!"

# Initialize the Kernel
kernel = Kernel()

# Add Azure OpenAI Chat Completion Service
chat_service = AzureChatCompletion(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    service_id="chat-service"
)
kernel.add_service(chat_service)

# Add the Plugin
plugin = SamplePlugin()
kernel.add_plugin(plugin, "SamplePlugin")

# Define the Chat Agent
agent = ChatCompletionAgent(
    kernel=kernel,
    name="SampleAgent",
    instructions="You are a helpful assistant with plugin capabilities.",
    arguments=KernelArguments()
)

# Example Usage
async def main():
    # Use the plugin
    plugin_response = await kernel.invoke_function("SamplePlugin.greet", {"name": "World"})
    print(f"Plugin Response: {plugin_response}")

    # Use the chat agent
    chat_response = await agent.get_response("What can you do?")
    print(f"Chat Agent Response: {chat_response.content}")

# Run the kernel and agent
import asyncio
asyncio.run(main())