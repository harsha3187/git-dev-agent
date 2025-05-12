from semantic_kernel import Kernel
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

# Define Agent 1
agent1 = ChatCompletionAgent(
    kernel=kernel,
    name="Agent1",
    instructions="You are an assistant for general queries.",
    arguments=KernelArguments()
)

# Define Agent 2
agent2 = ChatCompletionAgent(
    kernel=kernel,
    name="Agent2",
    instructions="You are an assistant specialized in GitHub-related queries.",
    arguments=KernelArguments()
)

# Example Usage
async def main():
    response1 = await agent1.get_response("What is the weather today?")
    print(f"Agent1: {response1.content}")

    response2 = await agent2.get_response("List the issues in the repository.")
    print(f"Agent2: {response2.content}")

# Run the agents
import asyncio
asyncio.run(main())