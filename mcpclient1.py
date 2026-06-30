import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():
    # Launch the filesystem MCP server
    server = StdioServerParameters(
        command="npx",
        args=[
            "@modelcontextprotocol/server-filesystem",
            "."
        ]
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the protocol
            await session.initialize()

            print("=" * 50)
            print("Connected successfully")
            print("=" * 50)

            # List available tools
            tools = await session.list_tools()

            print("\nAvailable Tools\n")

            for tool in tools.tools:
                print(f"Tool : {tool.name}")
                print(f"Description : {tool.description}")
                print("-" * 40)

            # Read a file
            print("\nReading test.txt...\n")

            result = await session.call_tool(
                "read_text_file",
                {
                    "path": "test.txt"
                }
            )

            print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
