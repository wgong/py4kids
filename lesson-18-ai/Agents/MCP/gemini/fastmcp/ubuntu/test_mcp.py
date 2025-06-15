#!/usr/bin/env python
# coding: utf-8

from fastmcp import Client
import asyncio

def format_tool(tool: dict):
    return f"""
[name]\t {tool.get("name")}
[description] {tool.get("description")}
"""

async def run_llm_demo(server_path: str = "mcp_server.py"):
    available_tools = []
    async with Client(server_path) as client:
        tools = await client.list_tools()
        # print(f"tools: {tools}\n")
        if tools:
            available_tools = [
                {"name": tool.name, "description": tool.description} for tool in tools
            ]
    return available_tools

resp = asyncio.run(run_llm_demo())


for r in resp:
    print(10*"*")
    print(format_tool(r))


