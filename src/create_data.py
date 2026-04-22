import os

from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def create_vector_store(client: AgentsClient) -> str:
    """Create a vector store with sample documents."""
    file_path = "./files/contoso-github-issues-guidelines.md"
    file = client.files.upload_and_poll(
        file_path=file_path, purpose="assistants"
    )

    vector_store = client.vector_stores.create_and_poll(
        file_ids=[file.id], name="contoso-github-issues-guidelines-vector-store"
    )

    return vector_store.id


def main():
    client = AgentsClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    vector_store_id = create_vector_store(client)
    print(f"Vector store created with ID: {vector_store_id}")


if __name__ == "__main__":
    main()