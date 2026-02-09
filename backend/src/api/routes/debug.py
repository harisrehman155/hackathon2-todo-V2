from fastapi import APIRouter, HTTPException, Request

from src.mcp.server import mcp


router = APIRouter(prefix="/api/debug", tags=["debug"])


@router.get("/mcp-tools")
async def list_mcp_tools(request: Request):
    settings = request.app.state.settings
    if settings.app_env.lower() != "development":
        raise HTTPException(status_code=404, detail="Not found")

    tools = await mcp.list_tools()
    return {
        "server": "Todo Tools",
        "count": len(tools),
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
                "output_schema": tool.outputSchema,
            }
            for tool in tools
        ],
    }
