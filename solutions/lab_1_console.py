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


async def main() -> None:
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

    print(f"User: {ISSUE_CONTEXT}")
    print("Agent: ", end="", flush=True)
    stream = issue_analyzer_agent.run(ISSUE_CONTEXT, stream=True)
    async for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
