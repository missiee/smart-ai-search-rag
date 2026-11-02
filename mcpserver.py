from mcp.server.fastmcp import FastMCP
from retrieval import search

mcp = FastMCP('docs-search')


@mcp.tool()
def search_docs(query: str, k: int = 5) -> str:
    '''Search the local knowledge base and return the most relevant passages.'''
    hits = search(query, k)
    return '\n\n'.join('[{}] {}'.format(h['source'], h['text']) for h in hits)


if __name__ == '__main__':
    mcp.run()