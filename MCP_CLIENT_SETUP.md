# MCP Client Setup Guide

This guide explains how to configure your MCP client (like Claude Desktop) to connect to your running Integration Platform API Server via ngrok.

## Server Information

- **Local Port:** `8020`
- **Ngrok URL:** `https://960e54f06392.ngrok-free.app`
- **SSE Endpoint:** `https://960e54f06392.ngrok-free.app/sse`

## Configuring Claude Desktop

To use this server with Claude Desktop:

1.  Open your Claude Desktop configuration file:
    - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
    - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

2.  Add the following configuration to the `mcpServers` object:

    ```json
    {
      "mcpServers": {
        "integration-api": {
          "url": "https://960e54f06392.ngrok-free.app/sse"
        }
      }
    }
    ```

3.  Save the file and restart Claude Desktop.

## Verifying Connection

Once Claude Desktop restarts, you should see the "integration-api" tools available. You can test it by asking Claude:
"List the available properties in the dev schema."

## Troubleshooting

- **502 Bad Gateway:** If you see this from ngrok, ensure your local server is running (`uv run -m api_server.api_server`).
- **Connection Refused:** Check if the port `8020` matches what the server is listening on.
