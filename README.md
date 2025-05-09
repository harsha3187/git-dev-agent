# 🤖 GitHub Chat Agent

The **GitHub Chat Agent** is a Streamlit-based application that allows users to interact with a GitHub repository in a conversational manner. It leverages **Semantic Kernel** and **Azure OpenAI** to provide intelligent responses and assist with repository queries. Additionally, it supports creating GitHub issues directly from the app.

---

## 🚀 Features

- **Chat with GitHub Repositories**: Query and retrieve information from a GitHub repository in a conversational format.
- **Create GitHub Issues**: Easily create issues in a repository with a user-friendly form.
- **Streamlit Interface**: Interactive and responsive UI for seamless user experience.
- **Azure OpenAI Integration**: Powered by Azure OpenAI for intelligent and context-aware responses.

---

## 📂 Directory Structure

```
git-chat-agent/
├── .devcontainer/          # Dev container configuration
│   ├── Dockerfile          # Dockerfile for the development container
│   ├── devcontainer.json   # Devcontainer configuration
├── app.py                  # Main Streamlit application
├── git_plugin.py           # Plugin for interacting with GitHub repositories
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── .env                    # Environment variables (not included in the repo)
```

---

## ✨ Features in Detail

### 💬 Chat with GitHub Repositories

- Query repository details in a conversational format.
- View chat history and interact with the assistant.

### 🐞 Create GitHub Issues

- Fill out a form to create issues in the repository.
- Add labels and descriptions for better issue tracking.

### 🧩 `git_plugin.py` - GitHub Interaction Plugin

The `git_plugin.py` file provides functionality to interact with GitHub repositories programmatically. It includes features such as:

- Fetching repository details (e.g., branches, commits, pull requests).
- Searching for files or content within the repository.
- Creating and managing GitHub issues.
- Authenticating with GitHub using a Personal Access Token (PAT).

This plugin is a core component of the application, enabling seamless integration with GitHub.

---

## 📓 Jupyter Notebook: `semantic-kernel-chat-agent.ipynb`

### Purpose
The  notebook provides an interactive environment to explore and experiment with the Semantic Kernel framework. It demonstrates how to use Semantic Kernel to build intelligent, context-aware chat agents and plugins for interacting with GitHub repositories.

### Features
- **Introduction to Semantic Kernel**:
  - Overview of key concepts like Kernel, Plugins, Agents, Chat Completion, and Vector Stores.
- **Chat Completion Service**:
  - Demonstrates how to create and interact with a chat completion service using Azure OpenAI.
- **Chat Completion Agent**:
  - Explains the difference between a chat completion service and an agent, and how to create an agent for context-aware interactions.
- **GitHub Plugin**:
  - Shows how to create a plugin to interact with the GitHub API for tasks like retrieving repository details, managing issues, and analyzing commits.
- **Practical Examples**:
  - Includes examples of querying user profiles, describing repositories, listing issues, and analyzing commits.

---

## 🛠️ Setup Instructions

### 🧑‍💻 Development with Dev Containers

This repository includes a `.devcontainer` configuration for Visual Studio Code. To use it:

1. Open the repository in VS Code.
2. Install the **Dev Containers** extension.
3. Reopen the project in the container.

### Local setup

### 1. Clone the Repository

```bash
git clone https://github.com/hannapureddy_microsoft/git-agent.git
cd git-chat-agent
```

### 2. Create a `.env` File

Create a `.env` file in the root directory by copying the `.env.example` file:

```bash
cp .env.example .env
```

Update the values in the `.env` file with your own credentials:

```plaintext
GLOBAL_LLM_SERVICE="AzureOpenAI"
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY="YOUR_API_KEY"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4.1"
AZURE_OPENAI_API_VERSION="2024-12-01-preview"
GITHUB_PAT="YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

---

## 🐳 Using Docker

### Build the Docker Image

```bash
docker build -f .devcontainer/Dockerfile -t git-chat-agent .
```

### Run the Docker Container

```bash
docker run -p 8501:8501 --env-file .env git-chat-agent
```

Access the app at [http://localhost:8501](http://localhost:8501).

---

## 🙌 Acknowledgments

- **Streamlit**
- **Semantic Kernel**
- **Azure OpenAI**
