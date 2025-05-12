from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

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

# Define the Agent
agent = ChatCompletionAgent(
    kernel=kernel,
    name="SampleAgent",
    instructions="You are a helpful assistant.",
    arguments=KernelArguments()
)

# Example Usage
async def main():
    response = await agent.get_response("Hello, how can you assist me?")
    print(response.content)

# Run the agent
import asyncio
asyncio.run(main())