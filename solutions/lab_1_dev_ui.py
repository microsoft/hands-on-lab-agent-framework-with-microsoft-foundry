import logging
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_devui import serve
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

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

    serve(entities=[issue_analyzer_agent], port=8090, auto_open=True)


if __name__ == "__main__":
    main()
