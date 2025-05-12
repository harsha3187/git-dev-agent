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
├── samples/                # Contains concepts samples
├── tutorial/               # Notebook file for step by step process of creating the kernel with plugins
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

## 📓 Jupyter Notebook: `tutorial/semantic-kernel-chat-agent.ipynb`

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

### 🧑‍💻 1. Development with Dev Containers

This repository includes a `.devcontainer` configuration for Visual Studio Code. To use it:

1. Open the repository in VS Code.
2. Install the **Dev Containers** extension.
3. Reopen the project in the container.

---

### 🧑‍💻 2. Local setup

### 2.1 Clone the Repository

```bash
git clone https://github.com/hannapureddy_microsoft/git-agent.git
cd git-chat-agent
```

### 2.2 Create a `.env` File

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
Follow these steps to create an Azure OpenAI endpoint and keys for Azure Open AI Model:

### 1. Create an Azure OpenAI Resource
1. Log in to the [Azure Portal](https://portal.azure.com/).
2. Search for **Azure OpenAI** in the search bar and select **Azure OpenAI**.
3. Click **Create** to start creating a new resource.
4. Fill in the required details:
   - **Subscription**: Select your Azure subscription.
   - **Resource Group**: Create a new resource group or select an existing one.
   - **Region**: Choose a supported region (e.g., East US, West Europe).
   - **Name**: Provide a unique name for your OpenAI resource.
5. Click **Review + Create** and then **Create**.

### 2. Deploy a model (ex:GPT-4.1)
1. Navigate to your newly created Azure OpenAI resource.
2. Go to the **Model Deployments** section in the left-hand menu.
3. Click **Create** to deploy a new model.
4. Select the **Model(ex:GPT-4.1)** model from the list.
5. Provide a **Deployment Name** (e.g., `gpt-4.1`) and configure the model settings as needed.
6. Click **Deploy** to start the deployment process.

### 3. Retrieve Endpoint and API Key
1. Once the deployment is complete, go to the **Keys and Endpoint** section in your Azure OpenAI resource.
2. Copy the **Endpoint URL** and **API Key**. These will be used in your `.env` file.

### Reference Image
Below is an example of the **Keys and Endpoint** section in the Azure portal:

<img width="854" alt="image" src="https://github.com/user-attachments/assets/16e7ff96-a584-4f74-80fa-ada4bb5a39e7" />

---

### 2.3 Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2.4 Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

---

## 🐳 3.Using Docker

### 3.1 Build the Docker Image

```bash
docker build -f .devcontainer/Dockerfile -t git-chat-agent .
```

### 3.2 Run the Docker Container

```bash
docker run -p 8501:8501 --env-file .env git-chat-agent
```

Access the app at [http://localhost:8501](http://localhost:8501).

---
### 🙌 Acknowledgments

- [**Streamlit**](https://streamlit.io/)
- [**Semantic Kernel**](https://github.com/microsoft/semantic-kernel)
- [**Azure OpenAI**](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/)
