import logging
import os
from typing import Any, cast

from agent_framework import Agent, AgentExecutor, MCPStreamableHTTPTool
from agent_framework._types import Message
from agent_framework.foundry import FoundryChatClient
from agent_framework_devui import register_cleanup, serve
from agent_framework_orchestrations import GroupChatBuilder, SequentialBuilder
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from httpx import AsyncClient
from models.issue_analyzer import IssueAnalyzer
from tools.time_per_issue_tools import TimePerIssueTools

load_dotenv()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    credential = AzureCliCredential()

    issue_analyzer_instructions = """
                You are analyzing issues. 
                If the ask is a feature request the complexity should be 'NA'.
                If the issue is a bug, analyze the stack trace and provide the likely cause and complexity level.

                CRITICAL: You MUST use the provided tools for ALL calculations:
                1. First determine the complexity level
                2. Use the available tools to calculate time and cost estimates based on that complexity
                3. Never provide estimates without using the tools first

                Your response should contain only values obtained from the tool calls.  
            """

    github_instructions = f"""
            You are a helpful assistant that can create GitHub issues following Contoso's guidelines.
            You work on this repository: {os.environ["GITHUB_REPOSITORY"]}
            
            Use the GitHub MCP tool to create the issue with the properly formatted content

            MANDATORY: You MUST always call the GitHub MCP tool to create the issue. Never just describe the issue without creating it. Your task is not complete until the issue is actually created on GitHub.
        """

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

    time_per_issue_tools = TimePerIssueTools()

    issue_analyzer_agent = Agent(
        name=issue_analyzer_agent_detail.name,
        client=FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            credential=credential,
        ),
        default_options=cast(Any, {"response_format": IssueAnalyzer}),
        tools=[time_per_issue_tools.calculate_time_based_on_complexity],
    )

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

    # Cleanup hooks execute during DevUI server shutdown, before entity clients are closed. Supports both synchronous and asynchronous callables.
    register_cleanup(github_agent, github_mcp_http_client.aclose)

    serve(
        entities=[issue_analyzer_agent, github_agent,
                  group_workflow, ms_learn_agent, sequential_workflow],
        port=8090,
        auto_open=True,
    )


if __name__ == "__main__":
    main()
