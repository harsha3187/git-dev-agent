import os
import streamlit as st
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from datetime import datetime
import asyncio

from git_plugin import GitHubPlugin, GitHubSettings

# Load environment variables
if os.path.exists(".env"):
    load_dotenv(override=True)

def get_kernel(repo_name):
    kernel = Kernel()
    service_id = "serv-git-chat-1"
    kernel.add_service(AzureChatCompletion(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        service_id=service_id
    ))
    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    gh_settings = GitHubSettings(token=os.getenv("GITHUB_PAT"))
    kernel.add_plugin(plugin=GitHubPlugin(gh_settings), plugin_name="GithubPlugin")
    inst_template = (
        "You are an agent designed to query and retrieve information from a single GitHub repository in a read-only manner.\n"
        "You are also able to access the profile of the active user.\n"
        "Use the current date and time to provide up-to-date details or time-sensitive responses.\n"
        "Use the values from arguments:\n"
        f"- The repository name: {repo_name}\n"
        f"- The current datetime: {datetime.now()}\n"
    )
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="GitAssistantAgent",
        instructions=inst_template,
        arguments=KernelArguments(settings=settings, repo_name=repo_name),
    )
    return agent

async def main():
    st.set_page_config(page_title="GitHub Chat Agent", layout="centered")
    st.title("🤖 GitHub Chat Agent")

    # Sidebar navigation
    with st.sidebar:
        with st.expander("🔎 Select Repository", expanded=True):
            repo_name = st.text_input("Repository (owner/repo):", st.session_state.get("repo_name", "harsha3187/git-dev-agent"))
            if repo_name != st.session_state.get("repo_name", ""):
                st.session_state.repo_name = repo_name
                st.session_state.agent = get_kernel(repo_name)
                st.session_state.chat_history = ChatHistory()  # Reset chat on repo change
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                # Add a message to chat history about repo change
                if len(st.session_state.messages) > 0:
                    repo_change_msg = f"🔄 Repository changed to **{repo_name}**."
                    st.session_state.messages.append({"role": "system", "content": repo_change_msg})
                    st.session_state.chat_history.add_message(
                        ChatMessageContent(role=AuthorRole.SYSTEM, content=repo_change_msg)
                    )

        # Navigation buttons
        page = st.radio(
            "Navigation",
            ["Chat", "Create GitHub Issue"],
            index=0,
            key="nav_radio"
        )

    # Session state for chat history and repo
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ChatHistory()
    if "repo_name" not in st.session_state:
        st.session_state.repo_name = "harsha3187/git-dev-agent"
    if "agent" not in st.session_state:
        st.session_state.agent = get_kernel(st.session_state.repo_name)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if page == "Chat":
        st.header(f"💬 Querying in \"{st.session_state.repo_name}\"")

        # Display chat history (streaming area at the top)
        chat_placeholder = st.container()
        with chat_placeholder:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Chat input at the bottom (use st.chat_input, which clears itself)
        st.markdown("---")
        prompt = st.chat_input("Type your message...")

        # Accept user input and stream assistant response
        if prompt:
            # Add user message to chat history and display
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.chat_history.add_message(
                ChatMessageContent(role=AuthorRole.USER, content=prompt)
            )
            with chat_placeholder:
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Stream assistant response
            with chat_placeholder:
                with st.chat_message("assistant"):
                    response_text = ""
                    response_container = st.empty()
                    with st.spinner("Thinking..."):
                        async def get_stream():
                            async for response in st.session_state.agent.invoke(messages=st.session_state.chat_history):
                                yield response.content
                        response_stream = get_stream()
                        async for chunk in response_stream:
                            response_text += str(chunk)
                            response_container.markdown(response_text)
                    st.session_state.chat_history.add_message(
                        ChatMessageContent(role=AuthorRole.ASSISTANT, content=response_text)
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

    elif page == "Create GitHub Issue":
        st.header("🐞 Create GitHub Issue")
        with st.form("issue_form"):
            issue_title = st.text_input("Issue Title")
            issue_desc = st.text_area("Issue Description")
            issue_labels = st.text_input("Labels (comma separated)")
            submit_issue = st.form_submit_button("Create Issue")
            if submit_issue and issue_title and issue_desc:
                gh_settings = GitHubSettings(token=os.getenv("GITHUB_PAT"))
                plugin = GitHubPlugin(gh_settings)
                labels = [l.strip() for l in issue_labels.split(",") if l.strip()]
                result = plugin.create_issue(
                    repo=st.session_state.repo_name,
                    title=issue_title,
                    body=issue_desc,
                    labels=labels
                )
                if result.get("html_url"):
                    st.success(f"Issue created: [View Issue]({result['html_url']})")
                else:
                    st.error("Failed to create issue.")

if __name__ == "__main__":
    asyncio.run(main())