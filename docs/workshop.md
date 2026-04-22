---
published: true
type: workshop
title: Product Hands-on Lab - Microsoft Agent Framework with Microsoft Foundry
short_title: Agent Framework with Microsoft Foundry
description: This workshop will cover how to build agentic applications using the Microsoft Agent Framework with Microsoft Foundry, leveraging various Azure services to create scalable and efficient solutions.
level: beginner # Required. Can be 'beginner', 'intermediate' or 'advanced'
navigation_numbering: true
authors: # Required. You can add as many authors as needed
  - Damien Aicheh
  - Olivier Mertens
  - David Rei
  - Amine Lemsih
contacts: # Required. Must match the number of authors
  - "@damienaicheh"
  - "@olmertens"
  - "@reidav"
  - "@aminelemsih"
duration_minutes: 300
tags: microsoft foundry, agent framework, mcp, ai search, foundry iq, dev-ui, csu, codespace, devcontainer
navigation_levels: 3
banner_url: assets/banner.jpg
audience: developers, architects, AI engineers

---

# Product Hands-on Lab - Microsoft Agent Framework with Microsoft Foundry

Welcome to this hands-on lab! In this workshop, you will learn how to build agentic applications using the Agent Framework with Microsoft Foundry. This workshop is available in Python, but don't forget that the *Microsoft Agent Framework* is also available in C#.

## What You Will Learn

In this hands-on lab, you will build a **Helpdesk Ops Assistant** powered by AI agents. This multi-agent system will handle internal support tickets by leveraging enterprise best practices (RAG), MCP servers, and native tools to provide intelligent assistance.

But firstly what's an AI agent?

An **AI agent** is a software component that uses a generative AI model to understand an input (a user request, an event, or another agent message), reasoning about what to do next, and then **take actions**.

In practice, an agent becomes useful when it can combine:

- **Knowledge** (for example, retrieving guidance or documentation)
- **Tools** (calling functions/APIs to do real work)

In this workshop, you will build multiple agents and orchestrate them so the system can analyze a ticket, look up relevant documentation, and create/update GitHub issues.

<div class="tip" data-title="Go deeper">

> If you want a broader (non-code) view of what an AI agent is and how to adopt agents in an organization, read:
> [AI agent adoption (Cloud Adoption Framework)](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/)
>
> It explains what makes agents different from classic RAG (agents decide *which* knowledge and tools to use step-by-step), outlines the core building blocks (model, instructions, retrieval/knowledge, actions/tools, memory), and provides guidance across the lifecycle: **plan**, **govern & secure**, **build**, and **operate** agents.

</div>

<details>
<summary><strong>Context (optional): Why agents are relevant here</strong></summary>

Helpdesk requests are mostly **unstructured text** (short descriptions, partial context, logs, mixed intents). Agents work well for this because they can:

- Extract structure from messy inputs (title, summary, root-cause hints) without a dedicated Natural Language Processing (NLP) pipeline.
- Combine reasoning with **tools** (deterministic calculations) and **RAG** (Retrieval-augmented generation), like company guidelines, internal documents, instead of relying on specific pre-trained models with your company knowledge.
- Adapt quickly as policies and documentation change (update the knowledge base and prompts, not a trained model).

Classic NLP/ML can be a great choice when you have stable categories and lots of labeled data (for example, high-volume ticket routing). For this workshop, the goal is an end-to-end assistant that can understand, retrieve context, and take actions rapidly with minimal setup.

</details>

### The Multi-Agent Architecture

You will create a multi-agent system built as a **sequence**: first the DocsAgent retrieves relevant documentation, then a **group chat** (managed by an orchestrator agent) coordinates the IssueAnalyzerAgent and GitHubAgent to complete the task.

[![architecture](./assets/architecture.png)](./assets/architecture.png)

**IssueAnalyzerAgent**  
Analyzes support tickets using structured data contracts (Pydantic models), determines issue complexity, and provides detailed analysis of bugs and feature requests. This agent uses native tools to calculate accurate time estimates based on complexity levels.

**GitHubAgent (MCP GitHub)**  
Executes GitHub ticketing actions (creating issues, adding labels, posting comments) based on the analysis provided by other agents. This agent leverages company-specific guidelines through RAG integration with a knowledge base.

**DocsAgent (MCP mslearn)**  
Queries Microsoft Learn documentation via MCP `mslearn` server to provide relevant documentation citations and technical guidance for issue resolution.

### Key Technologies

Throughout this workshop, you will:

- Build agentic applications using **[Microsoft Agent Framework][agent-framework-url]**
- Integrate **Microsoft Foundry** for AI model deployment and knowledge management
- Use **Retrieval-Augmented Generation (RAG)** with managed vector stores inside **Foundry IQ managed indexes**
- Use **Model Context Protocol (MCP)** servers for GitHub and Microsoft Learn integration
- Structure agent responses with **data contracts** using Pydantic models
- Create and use **native tools** for business logic (time estimation based on complexity)
- Orchestrate agents using **Group Chat patterns** and **Sequential Workflows**
- Leverage **Dev UI** for rapid agent development and testing

By the end of this lab, you will have a fully functional helpdesk system where multiple AI agents collaborate to analyze issues, retrieve relevant documentation, and manage tickets automatically following company guidelines.

[agent-framework-url]: https://github.com/microsoft/agent-framework

---

## Prerequisites

Before starting this lab, be sure to set your Azure environment :

- An Azure Subscription with the **Contributor** role to create and manage the labs' resources and deploy the infrastructure as code
- Register the Azure providers on your Azure Subscription if not done yet: `Microsoft.CognitiveServices`.

To retrieve the lab content :

- A GitHub account (Free, Team or Enterprise)
- Create a [fork][repo-fork] of the repository from the **main** branch to help you keep track of your changes

3 development options are available:
  - 🥇 *Preferred method* : Pre-configured GitHub Codespace 
  - 🥈 Local Devcontainer
  - 🥉 Local Dev Environment with all the prerequisites detailed below

<div class="tip" data-title="Tips">

> To focus on the main purpose of the lab, we encourage the usage of devcontainers/codespace as they abstract the dev environment configuration, and avoid potential local dependencies conflict.
>
> You could decide to run everything without relying on a devcontainer : To do so, make sure you install all the prerequisites detailed below.

</div>

### 🥇 : Pre-configured GitHub Codespace

To use a GitHub Codespace, you will need :

- [A GitHub Account][github-account]

GitHub Codespace offers the ability to run a complete dev environment (Visual Studio Code, Extensions, Tools, Secure port forwarding etc.) on a dedicated virtual machine.
The configuration for the environment is defined in the `.devcontainer` folder, making sure everyone gets to develop and practice on identical environments : No more conflict on dependencies or missing tools !

Every GitHub account (even the free ones) grants access to 120 vcpu hours per month, _**for free**_. A 2 vcpu dedicated environment is enough for the purpose of the lab, meaning you could run such environment for 60 hours a month at no cost!

To get your codespace ready for the labs, here are a few steps to execute :

- After you forked the repo, click on `<> Code`, `Codespaces` tab and then click on the `+` button:

![codespace-new](./assets/codespace-new.png)

- You can also provision a beefier configuration by defining creation options and select the **Machine Type** you like :

![codespace-configure](./assets/codespace-configure.png)

### 🥈 : Using a local Devcontainer

This repo comes with a Devcontainer configuration that will let you open a fully configured dev environment from your local Visual Studio Code, while still being completely isolated from the rest of your local machine configuration : No more dependancy conflict.
Here are the required tools to do so :

- [Git client][git-client]
- [Docker Desktop][docker-desktop] running
- [Visual Studio Code][vs-code] installed on your machine

Start by cloning the repository you just forked on your local Machine and open the local folder in Visual Studio Code.
Once you have cloned the repository locally, make sure Docker Desktop is up and running and open the cloned repository in Visual Studio Code.  

You will be prompted to open the project in a Dev Container. Click on `Reopen in Container`.

If you are not prompted by Visual Studio Code, you can open the command palette (`Ctrl + Shift + P`) and search for `Reopen in Container` and select it:

![devcontainer-reopen](./assets/devcontainer-reopen.png)

### 🥉 : Using your own local environment

The following tools and access will be necessary to run the lab on a local environment:  

<div class="tip" data-title="Windows note">

> If you're installing prerequisites with `winget`, open **Windows PowerShell as Administrator**.

</div>

- [Git client][git-client]
- [Visual Studio Code][vs-code] installed
- [Azure CLI][az-cli-install] installed on your machine
- [Python 3.13][download-python] installed on your machine
- [UV package manager][download-uv] installed on your machine
- [Terraform][download-terraform] installed on your machine

Visual Studio Code Extensions to install :

- [ms-python.python][ms-python-extension]
- [github.copilot][github-copilot-extension]
- [github.copilot-chat][github-copilot-chat-extension]
- [humao.rest-client][humao-rest-client-extension]
- [ms-python.vscode-pylance][ms-python-vscode-pylance-extension]
- [ms-vscode-remote.remote-containers][ms-vscode-remote-containers-extension]
- [charliermarsh.ruff][charliermarsh-ruff-extension]
- [ms-python.debugpy][ms-python-debugpy-extension]
- [hashicorp.terraform][hashicorp-terraform-extension]

Once you have set up your local environment, you can clone the repository you just forked on your machine, and open the local folder in Visual Studio Code and head to the next step.

### Sign in to Azure

> - Log into your Azure subscription in your environment using Azure CLI and on the [Azure Portal][az-portal] using your credentials.
> - Instructions and solutions will be given for the Azure CLI, but you can also use the Azure Portal if you prefer.
> - Register the Azure providers on your Azure Subscription if not done yet: `Microsoft.CognitiveServices`

```bash
# Login to Azure : 
# --tenant : Optional | In case your Azure account has access to multiple tenants

# Option 1 : Local Environment 
az login --tenant <yourtenantid or domain.com>
# Option 2 : Github Codespace : you might need to specify --use-device-code parameter to ease the az cli authentication process
az login --use-device-code --tenant <yourtenantid or domain.com>

# Display your account details
az account show
# Select your Azure subscription
az account set --subscription <subscription-id>

# Register the following Azure providers if they are not already
# Azure Cognitive Services
az provider register --namespace 'Microsoft.CognitiveServices'
```

### Deploy the infrastructure

First, you need to initialize the terraform infrastructure by running the following command:

```bash
# Run the following line which will dynamically set the subscription ID as an environment variable:
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Initialize terraform
cd infra && terraform init
```

Then run the following command to deploy the infrastructure:

```bash
# Apply the deployment directly
terraform apply -auto-approve
```

The deployment should take around 5 minutes to complete.

[ms-python-extension]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[github-copilot-extension]: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot
[github-copilot-chat-extension]: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat
[humao-rest-client-extension]: https://marketplace.visualstudio.com/items?itemName=humao.rest-client
[ms-python-vscode-pylance-extension]: https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance
[charliermarsh-ruff-extension]: https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff
[ms-python-bandit-extension]: https://marketplace.visualstudio.com/items?itemName=ms-python.bandit
[ms-python-debugpy-extension]: https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy
[hashicorp-terraform-extension]: https://marketplace.visualstudio.com/items?itemName=hashicorp.terraform
[ms-vscode-remote-containers-extension]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[az-cli-install]: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
[az-portal]: https://portal.azure.com
[vs-code]: https://code.visualstudio.com/
[azure-function-vs-code-extension]: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions
[docker-desktop]: https://www.docker.com/products/docker-desktop/
[repo-fork]: https://github.com/damienaicheh/hands-on-lab-agent-framework-on-azure/fork
[git-client]: https://git-scm.com/downloads
[github-account]: https://github.com/join
[download-python]: https://www.python.org/downloads/
[download-uv]: https://docs.astral.sh/uv/
[download-terraform]: https://developer.hashicorp.com/terraform/install

---

## Create your first agent

Let's create a first simple agent using the Agent Framework and a Foundry model to respond to basic queries.

Inside the `src` folder, you will find at root the `pyproject.toml` file that defines the dependencies for your Python project. Make sure to install them using `uv` and activate the virtual environment:

```bash
cd src
# Install dependencies and add .venv
uv sync
# Activate the virtual environment
source .venv/bin/activate
```

Then, rename the `.env.template` file to `.env` and update the environment variable `FOUNDRY_PROJECT_ENDPOINT` with the name of your Foundry instance from your deployed infrastructure. 

To connect to the AI chat model you need, you will use the Microsoft Foundry project resource to connect to the deployed models.

Go to [Azure Portal](https://portal.azure.com/#browse/all), inside your resource group, select the Microsoft Foundry project:

[![resource-group-foundry-project](./assets/resource-group-foundry-project.png)](./assets/resource-group-foundry-project.png)

Then select `Go to Foundry portal`:

![open-foundry-project](./assets/open-foundry-project.png)

You will be redirected to the home page of Microsoft Foundry Portal where you will have to copy paste the endpoint

<div class="tip" data-title="Microsoft Foundry portal">

> you can also directly go to the portal with this : [Microsoft Foundry](https://ai.azure.com/)

</div>

![foundry-project-endpoint](./assets/foundry-project-endpoint.png)

Then assign its value inside the `.env` file in the `FOUNDRY_PROJECT_ENDPOINT` environment variable.

When it's done, due to the role assigned to you on this cloud resource, you can have access to the models with your code.

Now let's create your first agent!

Inside `main.py` first, define the structure of the file and load the `.env` file and add the imports:

```python
import asyncio
import logging
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

ISSUE_CONTEXT = """
There is an issue with the Azure App Services is causing intermittent 500 errors. 
                        Traceback (most recent call last):
                                    File "<string>", line 38, in <module>
                                        main_application()                    ← Entry point
                                    File "<string>", line 30, in main_application
                                        results = process_data_batch(test_data)  ← Calls processor
                                    File "<string>", line 13, in process_data_batch
                                        avg = calculate_average(batch)        ← Calls calculator
                                    File "<string>", line 5, in calculate_average
                                        return total / count                  ← ERROR HERE
                                            ~~~~~~^~~~~~~
                                    ZeroDivisionError: division by zero
"""


async def main():
    logging.basicConfig(level=logging.ERROR, format="%(message)s")

    ## Create the agent here


if __name__ == "__main__":
    asyncio.run(main())
```

Then, let's create the first agent: IssueAnalyzerAgent, using the Agent Framework to analyze an ask.

Store the created agent version first, then reuse its returned name when instantiating the local `Agent`.

```python
credential = AzureCliCredential()

issue_analyzer_instructions = """
                You are analyzing issues. 
                If the ask is a feature request the complexity should be 'NA'.
                If the issue is a bug, analyze the stack trace and provide the likely cause and complexity level.
        """

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=credential,
)
model_name = os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"]

issue_analyzer_agent_detail = project.agents.create_version(
    agent_name="IssueAnalyzerAgent",
    definition=PromptAgentDefinition(
        model=model_name,
        instructions=issue_analyzer_instructions.strip(),
    ),
)

issue_analyzer_agent = Agent(
    name=issue_analyzer_agent_detail.name,
    client=FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    ),
)

print(f"User: {ISSUE_CONTEXT}")
print("Agent: ", end="", flush=True)
stream = issue_analyzer_agent.run(ISSUE_CONTEXT, stream=True)
async for chunk in stream:
    if chunk.text:
        print(chunk.text, end="", flush=True)
print("\n")
```

As you can see, to connect to Foundry and define the agent you have to use the `AIProjectClient` to create the agent in your Foundry project, then you can use the `FoundryChatClient` to connect to the model and run the agent.

Run the `main.py` file to see the output of your agent in the console:

```bash
uv run python main.py
```

The global variable `ISSUE_CONTEXT` contains the ask that you want to analyze, it can be a bug report with a stack trace or a feature request. The agent will analyze the ask and provide an answer based on the instructions you gave it.

You should see the question and agent answer like this in your terminal:

![agent-first-console](./assets/first-agent-console.png)

> The final `main.py` file can be found in `solutions/lab_1_console.py`.

To help you build and test your agent more easily, instead of relying only on the console output, let's introduce Dev UI integration.

Let's modify the `main.py` file to add Dev UI integration just after the agent creation.

First remove the `ISSUE_CONTEXT` which is not necessary anymore as you will be able to test the agent directly from Dev UI, then remove the entire `print` block you did previously and just replace it by this line: 

```python
serve(entities=[issue_analyzer_agent], port=8090, auto_open=True)
```

Remove the `async` keyword from the `main` function definition and the `asyncio.run(main())` at the end of the file as they are not necessary anymore.

Finally, add the import for the `serve` function at the top of the file:

```python
from agent_framework_devui import serve
```

<details>
<summary><strong>Information (optional): Dev UI </strong></summary>

If you want to discover more about Dev UI, you can follow the official tutorial:
[Dev UI on Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/user-guide/devui/?pivots=programming-language-python)

</details>

Now if you run your agent again:

```bash
uv run python main.py
```

Let's run the agent with a simple prompt to analyze a first ask,(this can be found in the `src/PROMPT_ISSUE_SAMPLE.md` file, keep it open as you will need it for the next steps):

```txt
There is an issue with the Azure App Services is causing intermittent 500 errors. 
                        Traceback (most recent call last):
                                    File "<string>", line 38, in <module>
                                        main_application()                    ← Entry point
                                    File "<string>", line 30, in main_application
                                        results = process_data_batch(test_data)  ← Calls processor
                                    File "<string>", line 13, in process_data_batch
                                        avg = calculate_average(batch)        ← Calls calculator
                                    File "<string>", line 5, in calculate_average
                                        return total / count                  ← ERROR HERE
                                            ~~~~~~^~~~~~~
                                    ZeroDivisionError: division by zero
```

Open your browser and go to `http://localhost:8090` to access the Dev UI. You should see your agent listed there (in the dropdown list at the top of your screen). Click on it to open the chat interface.

[![issue_agent_tool_devui_start.png](./assets/issue_agent_tool_devui_start.png)](./assets/issue_agent_tool_devui_start.png)

If you try to run the agent multiple times, you might hit the rate limit of tokens per minute. If that happens, you will see a 429 error. Just wait a minute or two and try again.

Also, if you look at the output, the response is always different because the model is generative and non-deterministic by default, but you ask the model to structure the output in a specific format. That's what you will do in the next step.

If you go on your Foundry project, because we used the `FoundryChatClient`, you will see your agent instantiated inside the **Build** tab, under the **Agents** section:

[![foundry-first-agent](./assets/foundry-first-agent.png)](./assets/foundry-first-agent.png)

You can click on it to see the details of the agent and its activity, and also to test it directly from there without going through Dev UI.

> The final `main.py` file can be found in `solutions/lab_1_dev_ui.py`.

---

## Add response format

Let's structure the output of your agent to make it more useful and more programmatic.

To make sure the *IssueAnalyzerAgent* provide the same structure every time, let's define a response format using a basic python class.

Inside the `src` folder, create a new folder called `models` and inside this folder create a new file called `issue_analyzer.py`.

```python
from enum import Enum

from pydantic import BaseModel


class Complexity(str, Enum):
    NA = "NA"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class IssueAnalyzer(BaseModel):
    """Information about an issue."""
    title: str | None
    description: str | None
    reason: str | None
    complexity: Complexity | None
    time_estimate_hours: str | None
```

As you can see, the `IssueAnalyzer` class defines multiple fields that the agent will fill when answering a prompt.

Now, let's modify the `main.py` file to use this response format. Inside the `Agent` object (just after the `client` parameter), add the `response_format` parameter:

```python
default_options=cast(Any, {"response_format": IssueAnalyzer}),
```

Also, make sure to import the missing classes at the top of the file:

```python
from typing import Any, cast
from models.issue_analyzer import IssueAnalyzer
```

You can now run your agent again:

```bash
uv run python main.py
```

<div class="tip" data-title="Tip: stop an old run before relaunching">

> If you already ran `uv run python main.py`, Dev UI may still be running in another terminal.
> Stop it with `Ctrl+C`, then run the command again.
>
> If the port is still busy, find and kill the process using port `8090`:
>
> ```bash
> lsof -i :8090
> kill <pid>
> ```

</div>

You should notice that the output is now structured according to the `IssueAnalyzer` class you defined.

As you can see in the Dev UI, the output is now in JSON format, making it easier to parse and use in other agents or systems:

[![devui-structured-output](./assets/issue_agent_tool_devui_json.png)](./assets/issue_agent_tool_devui_json.png)

> The final `main.py` file can be found in `solutions/lab_2.py`.

---

## Add native tools

If you looked at the output of your agent, you probably noticed that the estimated time to resolve the issue is randomly generated by the model. To make it more accurate, let's add a native tool that will help the agent estimate the time based on the complexity of the issue.
Don't forget that tools are pieces of code, calls to Apis, or calling agents, MCP ... that can be called by the agent to perform specific tasks.

First, create a new folder called `tools` inside the `src` folder. Then, inside this folder, create a new file called `time_per_issue_tools.py`.

```python
from typing import Annotated

from models.issue_analyzer import Complexity
from pydantic import Field


class TimePerIssueTools:

    def calculate_time_based_on_complexity(
        self,
        complexity: Annotated[Complexity, Field(description="The complexity level of the issue.")],
    ) -> str:
        """Calculate the time required based on issue complexity."""
        match complexity:
            case Complexity.NA:
                return "1 hour"
            case Complexity.LOW:
                return "2 hours"
            case Complexity.MEDIUM:
                return "4 hours"
            case Complexity.HIGH:
                return "8 hours"
            case _:
                return "Unknown complexity level"
```

This class defines a single tool that calculates the estimated time to resolve an issue based on its complexity. Of course, you can implement more tools as needed, with API calls or other logic.

Now, let's modify the `main.py` file to add this tool to your agent.

First, add the imports at the top of the file:

```python
from tools.time_per_issue_tools import TimePerIssueTools
```

Then before the agent creation, create an instance of the `TimePerIssueTools` class:

```python
time_per_issue_tools = TimePerIssueTools()
```

Inside the agent creation add the tools properties:

```python
tools=[time_per_issue_tools.calculate_time_based_on_complexity],
```

Also, let's update the instructions to give more details to the agent on how to use this tool:

```python
instructions="""
    You are analyzing issues. 
    If the ask is a feature request the complexity should be 'NA'.
    If the issue is a bug, analyze the stack trace and provide the likely cause and complexity level.

    CRITICAL: You MUST use the provided tools for ALL calculations:
    1. First determine the complexity level
    2. Use the available tools to calculate time and cost estimates based on that complexity
    3. Never provide estimates without using the tools first

    Your response should contain only values obtained from the tool calls.
""",
```

Now, run your agent again:

```bash
uv run python main.py
```

<div class="task" data-title="Try it: test the agent within its scope">

> In Dev UI, select **IssueAnalyzerAgent** and try the prompt from the `src/PROMPT_ISSUE_SAMPLE.md` file like previously.
>
> Verification: open the **Tools** tab and confirm you see a call to `calculate_time_based_on_complexity`.

</div>

As you can see in the `Tools` tab of Dev UI, the agent used the `calculate_time_based_on_complexity` tool to estimate the time to resolve the issue based on its complexity. If you look at the **Tools** tab, you should see the tool being called with the complexity level and the estimated time being returned:

[![devui-tools-tab](./assets/issue_agent_tool_devui.png)](./assets/issue_agent_tool_devui.png)

Your *IssueAnalyzerAgent* is now more precise and reliable!

> The final `main.py` file can be found in `solutions/lab_3.py`.

---

## Add MCP tool

You have now a first agent to analyze issues and request of users, but to build a complete helpdesk solution, you need to add another agent responsible of adding the query as a ticket. For the purpose of this workshop, you will use your own GitHub repository as a ticketing system, using GitHub Issues.

To do that, you will use the MCP GitHub tool provided by GitHub and create a new agent called GitHubAgent.

<details>
<summary><strong>Context (optional): What is MCP and why do we use it?</strong></summary>

**MCP (Model Context Protocol)** is a standard way for an AI agent to connect to external capabilities.

Think of it like a **USB-C dongle**:

- Your laptop has one USB-C port (the agent/runtime).
- The dongle gives you many ports (capabilities): GitHub, file systems, web search, internal services, etc.
- Each “port” maps to **tools** that the agent can call in a structured, permissioned way.

In practice, an MCP server can expose:

- **Tools** (functions) like “create GitHub issue”, “list issues”, “add label”, “comment on an issue”.
- **API wrappers** that hide authentication and request details.
- Sometimes even **other agents or services** behind the server (the agent just calls a tool; the server decides what happens next).

Purpose: keep the agent focused on reasoning, while MCP provides the safe, reusable bridge to real actions and data.

If you want to go deeper:

- [MCP for Beginners (GitHub)](https://github.com/microsoft/mcp-for-beginners/)
- [MCP overview video (YouTube)](https://www.youtube.com/watch?v=VfZlglOWWZw&t=3s)

</details>

### Get Personal Access Token (PAT) for the GitHub MCP server

To authenticate to GitHub, you need to create a Personal Access Token (PAT) with the appropriate permissions. This PAT will only need to have access to your repository (result of the fork you did at the beginning of the workshop) and read/write access to issues.
This PAT is personal to your github account and will be used by the GitHub MCP tool to authenticate requests to GitHub.

To do so, go to your GitHub account settings by clicking on your profile picture, then click on **Settings**.

At the bottom go to **Developer Settings** > **Personal Access Tokens** > **Fine-grained tokens** and create a new token with the following settings:

- Give it a name, e.g., `Agent Framework Workshop Token`
- Set the expiration to `30 days`
- Under **Repository access**, select `Only select repositories` and choose the repository you forked
- Under **Permissions**, set the following:
  - Issues: `Read and write`

Finally click on **Generate token**.

[![github-create-pat](./assets/github-create-pat.png)](./assets/github-create-pat.png)

Once the token is created, make sure to copy it and put it inside the `GITHUB_MCP_PAT` environment variable in your `.env` file.

You are now ready to use the GitHub MCP tool in your agent!

Go back to your Python project and set the `GITHUB_REPOSITORY` environment variable to the format `owner/repo`, e.g., `your-username/your-forked-repo`.

Make sure to enable the issues on your GitHub repository as well, otherwise the GitHubAgent won't be able to create issues. To do that, go to your repository on GitHub, click on **Settings** > **Features** and make sure the **Issues** feature is enabled.

### Create the GitHubAgent

Now, let's create the GitHubAgent inside the `main.py` file. Just after the creation of the IssueAnalyzerAgent, add the following code:

```python
github_instructions = f"""
        You are a helpful assistant that can create GitHub issues following Contoso's guidelines.
        You work on this repository: {os.environ["GITHUB_REPOSITORY"]}
        
        Use the GitHub MCP tool to create the issue with the properly formatted content

        MANDATORY: You MUST always call the GitHub MCP tool to create the issue. Never just describe the issue without creating it. Your task is not complete until the issue is actually created on GitHub.
    """

github_agent_detail = project.agents.create_version(
    agent_name="GitHubAgent",
    definition=PromptAgentDefinition(
        model=model_name,
        instructions=github_instructions.strip(),
    ),
)

github_chat_client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
    credential=credential,
)

github_mcp_http_client = AsyncClient(
    headers={
        "Authorization": f"Bearer {os.environ['GITHUB_MCP_PAT']}",
        "Accept": "application/json, text/event-stream",
    }
)

github_agent = Agent(
    name=github_agent_detail.name,
    client=github_chat_client,
    tools=[
        MCPStreamableHTTPTool(
            name="GitHub",
            url="https://api.githubcopilot.com/mcp/",
            approval_mode="never_require",
            http_client=github_mcp_http_client,
        ),
    ],
)
```

Don't forget to import the missing classes at the top of the file:

```python
from agent_framework import Agent, MCPStreamableHTTPTool
from httpx import AsyncClient
```

As you can see, you dynamically load the MCP GitHub tool and create the agent using this tool. The `AsyncClient` is used to make asynchronous HTTP requests to the MCP server, and the authorization header is set with the PAT you created earlier.

Finally, as you did for the IssueAnalyzerAgent, add the GitHubAgent to the Dev UI integration:

```python
# Cleanup hooks execute during DevUI server shutdown, before entity clients are closed. Supports both synchronous and asynchronous callables.
register_cleanup(github_agent, github_mcp_http_client.aclose)

serve(entities=[issue_analyzer_agent, github_agent], port=8090, auto_open=True)
```

And the missing import for the `register_cleanup` function:

```python
from agent_framework_devui import register_cleanup
```

Now, run your agent again:

```bash
uv run python main.py
```

Select the *GitHubAgent* in the Dev UI and ask your first question:

[![select-menu-devui](./assets/devui_select_menu.png)](./assets/devui_select_menu.png)

If you ask the agent to create an issue about any kind of problem, it should create a new issue in your GitHub repository!

[![initial-issue-created](./assets/initial-issue-creation.png)](./assets/initial-issue-creation.png)

The GitHubAgent is also available in your Foundry project under the **Agents** section.

> The final `main.py` file can be found in `solutions/lab_4.py`.

---

## Create a group chat workflow

You have now two agents: the *IssueAnalyzerAgent* to analyze issues and the *GitHubAgent* to create tickets in GitHub. To build a complete helpdesk solution, you need to orchestrate these two agents to work together in a group chat.

To do that you will use a mechanism called Group Chat Workflow provided by the Agent Framework.

This will allow the agents to communicate and collaborate to handle asks in their own chat.

Let's create the chat group inside the `main.py` file.

First import the `GroupChatBuilder` class at the top of the file:

```python
from agent_framework.orchestrations import GroupChatBuilder
```

Just after the creation of the GitHubAgent, add the following code:

```python
orchestrator_instructions = """
            You are a workflow manager that coordinates issue creation.
            Decide which participant should speak next.

            Output rules are mandatory:
            - Return ONLY one raw JSON object.
            - Do NOT wrap JSON in markdown fences.
            - Do NOT add extra text before or after JSON.
            - Use exactly these keys: terminate, reason, next_speaker, final_message.
            - If terminate is false, next_speaker must be one of: IssueAnalyzerAgent, GitHubAgent.

            Workflow policy:
            1. Ask IssueAnalyzerAgent first to classify and estimate complexity.
            2. Then ask GitHubAgent to create the issue.
            3. Do NOT terminate until GitHubAgent has actually created the issue on GitHub and provides a link or confirmation.
            4. If GitHubAgent only describes the issue without creating it, ask GitHubAgent again to create it.
        """
        
orchestrator_agent_detail = project.agents.create_version(
    agent_name="IssueCreatorOrchestratorAgent",
    definition=PromptAgentDefinition(
        model=model_name,
        instructions=orchestrator_instructions.strip(),
    ),
)

orchestrator_agent = Agent(
    name=orchestrator_agent_detail.name,
    client=FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    ),
    default_options={"temperature": 0},
)

group_workflow = GroupChatBuilder(
    participants=[issue_analyzer_agent, github_agent],
    intermediate_outputs=True,
    orchestrator_agent=orchestrator_agent,
).build()
```

As you can see, you create a group chat workflow with the *IssueAnalyzerAgent* and the *GitHubAgent*. The agents are guided by a manager agent that will route the requests to the appropriate agent based on the prompt.

Now, update the Dev UI setup to add the group chat workflow instead of the individual agents:

```python
serve(entities=[issue_analyzer_agent, github_agent, group_workflow], port=8090, auto_open=True)
```

Now, run your agent again:

```bash
uv run python main.py
```

In the dropdown menu of Dev UI, you should now see in the workflow section your group chat workflow, select it and click on `Configure & Run` to test it.
A pop-up will open, you can enter the same prompt as before to test the workflow in the `contents` section and `user` in the role section:

[![run-workflow-dev-ui](./assets/run-workflow-dev-ui.png)](./assets/run-workflow-dev-ui.png)

Then click on `Run` :

[![group-orchestration-workflow](./assets/group-orchestration-workflow.png)](./assets/group-orchestration-workflow.png)

You can now interact with the group chat workflow. The manager agent will route your requests to the appropriate agent based on the prompt.

At the time of writing this tutorial workflow created by Microsoft Agent Framework are not reflected in Foundry only the **IssueCreatorOrchestrator** will be visible in Foundry.

> The final `main.py` file can be found in `solutions/lab_5.py`.

---

## Orchestrate with a sequential workflow

Let's go a step further and add one more agent in the picture. You will add a *DocsAgent* that will provide relevant documentation from Microsoft Learn to help the agents answer user requests. This agent will use the MCP Learn tool.

First, create the *DocsAgent* inside the `main.py` file. Just after the creation of the GitHubAgent, add the following code:

```python
ms_learn_instructions = """
        You are a Microsoft documentation assistant.
        Mandatory rules:
        1. You must call the Microsoft Learn MCP tool before answering any user question.
        2. You are not allowed to answer from internal knowledge alone.
        3. Your final answer must be grounded only in Microsoft Learn MCP results.
        4. If no relevant result is found, explicitly say the information was not found in Microsoft Learn.
        5. If the tool is unavailable or fails, do not guess or fabricate; state that you cannot answer without Microsoft Learn MCP.
        6. Keep responses concise, accurate, and factual.
    """

docs_agent_detail = project.agents.create_version(
    agent_name="DocsAgent",
    definition=PromptAgentDefinition(
        model=model_name,
        instructions=ms_learn_instructions.strip(),
    ),
)

ms_learn_agent = Agent(
    name=docs_agent_detail.name,
    client=FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    ),
    tools=[
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            terminate_on_close=False,
        )
    ],
)
```

As you can see, you dynamically load the MCP Learn tool, without authentication for this one, as it is totally open, and create the agent using this tool.

Then convert the group chat workflow you created in the previous step into an agent so it can be called inside another workflow:

```python
group_workflow_agent = group_workflow.as_agent(
    name="IssueCreationAgentGroup"
)

def _flatten_handoff_to_user_message(messages: list[Message]) -> list[Message]:
    # Pass only plain text to the next step so it doesn't inherit MCP tool-call artifacts.
    combined_text = "\n\n".join(
        message.text for message in messages if message.text)
    return [Message(role="user", contents=[combined_text])] if combined_text else messages

sequential_workflow = SequentialBuilder(
    participants=[
        ms_learn_agent,
        AgentExecutor(
            group_workflow_agent,
            context_mode="custom",
            context_filter=_flatten_handoff_to_user_message,
        ),
    ],
).build()
```

The `_flatten_handoff_to_user_message` function is used to rewrite the context between agents, it takes the output of the first agent and formats it as a user message for the next agent, stripping any tool-call noise that might be present in the intermediate outputs.

The `SequentialBuilder` is used to create a sequential workflow that will first call the *DocsAgent* and then the group of agents represented by the *IssueCreationAgentGroup*, containing the *IssueAnalyzerAgent* and the *GitHubAgent*.

Add the missing imports at the top of the file:

```python
from agent_framework import Agent, AgentExecutor, MCPStreamableHTTPTool
from agent_framework._types import Message
from agent_framework_orchestrations import SequentialBuilder
from agent_framework_devui import register_cleanup, serve
```

If you want to test it individually, you can update the Dev UI integration:

```python
serve(
    entities=[issue_analyzer_agent, github_agent,
                group_workflow, ms_learn_agent, sequential_workflow],
    port=8090,
    auto_open=True,
)
```

Finally, run your agent again:

```bash
uv run python main.py
```

Select the sequential workflow agent in the Dev UI and ask your first question:

[![sequential-workflow-devui](./assets/sequential-orchestration-workflow.png)](./assets/sequential-orchestration-workflow.png)

The **DocsAgent** will be visible inside Foundry.

> The final `main.py` file can be found in `solutions/lab_6.py`.

<details>
<summary><strong>Information (optional): Workflow pattern explained </strong></summary>

This lab explained the Group Chat and Sequential Workflows patterns. If you want to go deeper, follow the official samples with the different workflow patterns:

[Microsoft Agent Framework Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview)

</details>

---

## Add your own knowledge base with RAG

You now have a complete helpdesk solution with multiple agents working together to handle user requests. However, the GitHubAgent is doing some ticketing without really knowing your company's (named Contoso) conventions and best practices. To improve this, you will add another source of knowledge using *Retrieval-Augmented Generation* (RAG) with your Microsoft Foundry project.

To do that, you will find a file called `create_data.py` in the `src` folder that will help you create a managed knowledge base inside Foundry IQ based on best practices in a file inside the folder `files`. This file symbolizes the internal documentation that your company can have about how to create good tickets, and the agent will be able to retrieve this information to create tickets that are more compliant with company standards.

```bash
uv run python create_data.py
```

This will create a managed index for you that will be used as a knowledge base for your GitHubAgent. Look at the console output to get the vector store ID created and set the environment variable `VECTOR_STORE_ID` with this value in the `.env` file.

To see the index generated, go to your Microsoft Foundry project, select **Build** > **Data** > **Datasets** and you should see the dataset created:

[![Datasets](./assets/foundry-project-datasets.png)](./assets/foundry-project-datasets.png)

In the **Knowledge** tab, you should see the managed index made by Foundry IQ created:

[![Managed Index](./assets/foundry-iq-managed-index.png)](./assets/foundry-iq-managed-index.png)

Foundry IQ hide the complexity of managing a knowledge base for you, making it easy to create and maintain. You can also connect other sources of knowledge like [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search).

Now, let's modify the *GitHubAgent* to use this knowledge base when answering user requests. Inside the creation of the *GitHubAgent*, add the following code to retrieve the data tool:

Before the GitHub Agent creation add the file search tool with the vector store ID as input:

```python
file_search_tool = github_chat_client.get_file_search_tool(
    vector_store_ids=[os.environ["VECTOR_STORE_ID"]]
)
```

Then update the agent creation with this tool:

```python
github_agent = Agent(
    name=github_agent_detail.name,
    client=github_chat_client,
    tools=[
        file_search_tool,
        MCPStreamableHTTPTool(
            name="GitHub",
            url="https://api.githubcopilot.com/mcp/",
            approval_mode="never_require",
            http_client=github_mcp_http_client,
        ),
    ],
)
```

and finally update the instructions to inform the agent about the knowledge base:

```python
github_instructions = f"""
            You are a helpful assistant that can create GitHub issues following Contoso's guidelines.
            You work on this repository: {os.environ["GITHUB_REPOSITORY"]}

            CRITICAL WORKFLOW:
            1. ALWAYS use the File Search tool FIRST to search for "github issues guidelines" or "issue template" to find the proper formatting and structure
            2. Follow the Contoso GitHub Issues Guidelines found in the vector store
            3. Use the retrieved guidelines to format the issue properly with correct structure, labels, and format
            4. Then use the GitHub MCP tool to create the issue with the properly formatted content

            IMPORTANT: You MUST search for guidelines BEFORE creating any issue to ensure compliance with company standards.
            MANDATORY: You MUST always call the GitHub MCP tool to create the issue. Never just describe the issue without creating it. Your task is not complete until the issue is actually created on GitHub.
        """
```

**Don't forget that the agent must know the element of tools, knowledge base, etc ... to be able to use them properly.**

You can now run the project and test the full workflow or the GitHubAgent individually:

```bash
uv run python main.py
```

You should have issues created with a more profesionnal format (stacktrace, step to reproduce, etc.)

[![final-issue-creation](./assets/final-issue-creation.png)](./assets/final-issue-creation.png)

> The final `main.py` file can be found in `solutions/lab_7.py`.

---

## Monitor and troubleshoot your Agents

To monitor and troubleshoot your agents, you can leverage the observability features provided by the Agent Framework to display logs and traces inside Azure Application Insights.

First, let's add the import for the logging module at the top of the `main.py` file:

```python
from agent_framework.observability import (
    create_resource,
    enable_instrumentation,
    get_tracer,
)
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.trace import SpanKind, format_trace_id
```

Then, as update the `__main__` section to add the following code to set up observability:

```python
if __name__ == "__main__":
    configure_azure_monitor(
        connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
        enable_live_metrics=True,
        resource=create_resource(),
        enable_performance_counters=False,
    )
    enable_instrumentation(enable_sensitive_data=True)
    with get_tracer().start_as_current_span("Issue Analyzer Agent Workflow", kind=SpanKind.CLIENT) as current_span:
        print(
            f"Trace ID: {format_trace_id(current_span.get_span_context().trace_id)}")
        main()
```

That's it for the Python code! Then update the value of the `APPLICATIONINSIGHTS_CONNECTION_STRING` key in the `.env` file with the Application Insights connection string. You can find it in the Azure Portal inside your resource group, in the Application Insights resource created by the Terraform deployment.

[![app-insights-connection-string](./assets/app-insights-connection-string.png)](./assets/app-insights-connection-string.png)

Now, run workflow again and play with it:

```bash
uv run python main.py
```

Now if you go to the Application Insights resource in the Azure Portal, you should see the logs and traces generated by the agents:

[![application-insights-agents](./assets/application-insights-agents.png)](./assets/application-insights-agents.png)

If you click on **View Traces with Agent Runs** you will be able to see the traces of your agents, select one of the traces to see more details:

[![application-insights-traces-table](./assets/application-insights-traces-table.png)](./assets/application-insights-traces-table.png)

You will be able to see the full trace of the agent run, like tool calls, and any errors that might have occurred:

[![application-insights-transaction](./assets/application-insights-transaction.png)](./assets/application-insights-transaction.png)

> The final `main.py` file can be found in `solutions/lab_8.py`.

---

## Closing the workshop

Once you're done with this lab you can delete the resource group you created at the beginning.

To do so, click on **Delete resource group** in the Azure Portal to delete all the resources at once. The following Az-Cli command can also be used to delete the resource group:

```bash
# Delete the resource group with all the resources
az group delete --name <resource-group>
```

<details>
<summary><strong>Information (optional): Time to brag </strong></summary>

If you have finished you gained a GG from our mascot Bits !

[![gg-mascott](./assets/xmasbit.jpeg)](./assets/xmasbit.jpeg)

</details>

---

## Takeaways

Congratulations! You have successfully completed this hands-on lab on building agentic applications on Azure using Microsoft Foundry and the Agent Framework SDK. To explore more advanced Agent Framework capabilities, consider checking out the following resources:

**Additional Resources:**

- [Agent framework for beginners](https://aka.ms/ai-agents-beginners)
- [Get Started with Agent Framework](https://aka.ms/AgentFramework)
- [Agent Framework Documentation](https://aka.ms/AgentFramework/Docs)
- [Announcement Blog Agent framework](https://aka.ms/AgentFramework/PuPr)
- [Watch Sessions On-Demand Agent framework](https://aka.ms/AgentFramework/AIShow)
- [MCP for Beginners (GitHub)](https://github.com/microsoft/mcp-for-beginners/)
- [MCP overview video (YouTube)](https://www.youtube.com/watch?v=VfZlglOWWZw&t=3s)

