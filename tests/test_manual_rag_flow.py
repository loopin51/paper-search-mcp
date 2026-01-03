import asyncio
import sys
import os

# Ensure we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paper_search_mcp.server import rag_create_session, rag_add_paper, rag_query

async def main():
    print("Creating session...")
    session_id = await rag_create_session()
    print(f"Session ID: {session_id}")
    
    # Use 'Attention Is All You Need'
    paper_id = "1706.03762"
    print(f"Adding paper {paper_id}...")
    
    # This might take time (downloading PDF + downloading models + processing)
    # Set a timeout for the user's sake in thought process, but let it run here.
    result = await rag_add_paper(session_id, paper_id, platform="arxiv")
    print(f"Add result: {result}")
    
    if "Failed" in result:
        print("Test Failed at adding paper.")
        return

    print("Querying: 'What is the attention mechanism?'")
    results = await rag_query(session_id, "What is the attention mechanism?")
    
    print("\nQuery Results:")
    for i, chunk in enumerate(results):
        print(f"--- Result {i+1} (Score: {chunk.get('score', 'N/A')}) ---")
        text = chunk.get('text', '')
        print(text[:200] + "..." if len(text) > 200 else text)
        print()

if __name__ == "__main__":
    asyncio.run(main())
