import logging
import os
from typing import Any, cast

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_devui import serve
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

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

    serve(entities=[issue_analyzer_agent], port=8090, auto_open=True)


if __name__ == "__main__":
    main()
