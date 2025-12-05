from fastapi import FastAPI
from fastmcp import FastMCP
import os

TITLE = os.getenv("MCP_TITLE", "Python MCP Template")
DESCRIPTION = os.getenv(
    "MCP_DESCRIPTION", "A template for creating MCP-compliant FastAPI"
)

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
)


@app.post("new_endpoint")
async def new_endpoint(name: str):
    """

    Parameters
    ----------
    name : str
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return {"message": "This is a new endpoint!"}


mcp = FastMCP.from_fastapi(app=app)

if __name__ == "__main__":
    mcp.run()
