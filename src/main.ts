#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

import { Server } from "npm:@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "npm:@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "npm:@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "mcp-notes",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

server.setRequestHandler(ListToolsRequestSchema, () => {
  const tools: Tool[] = [
    {
      name: "create_note",
      description: "Create a new markdown note with YAML frontmatter in the Obsidian vault",
      inputSchema: {
        type: "object",
        properties: {
          title: {
            type: "string",
            description: "Title of the note",
          },
          content: {
            type: "string",
            description: "Main content of the note",
          },
          tags: {
            type: "array",
            items: { type: "string" },
            description: "Tags to associate with the note",
          },
          conversation_id: {
            type: "string",
            description: "ID of the conversation this note relates to",
          },
          ai_client: {
            type: "string",
            description: "Name of the AI client used",
          },
          summary: {
            type: "string",
            description: "Brief summary of the note content",
          },
        },
        required: ["title", "content"],
      },
    },
    {
      name: "search_notes",
      description: "Search through existing notes using full-text search",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Search query text",
          },
          tags: {
            type: "array",
            items: { type: "string" },
            description: "Filter by specific tags",
          },
          limit: {
            type: "number",
            description: "Maximum number of results to return",
            default: 10,
          },
        },
        required: ["query"],
      },
    },
    {
      name: "list_notes",
      description: "List notes with optional filtering and sorting",
      inputSchema: {
        type: "object",
        properties: {
          tags: {
            type: "array",
            items: { type: "string" },
            description: "Filter by specific tags",
          },
          limit: {
            type: "number",
            description: "Maximum number of notes to return",
            default: 20,
          },
          sort: {
            type: "string",
            enum: ["created", "updated", "title"],
            description: "Sort field",
            default: "updated",
          },
          order: {
            type: "string",
            enum: ["asc", "desc"],
            description: "Sort order",
            default: "desc",
          },
        },
      },
    },
    {
      name: "get_note",
      description: "Retrieve the full content of a specific note",
      inputSchema: {
        type: "object",
        properties: {
          filename: {
            type: "string",
            description: "Filename of the note to retrieve",
          },
        },
        required: ["filename"],
      },
    },
  ];

  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, (request) => {
  const { name } = request.params;

  try {
    switch (name) {
      case "create_note":
        // TODO: Implement create_note tool
        return {
          content: [
            {
              type: "text" as const,
              text: "create_note tool not yet implemented",
            },
          ],
        };

      case "search_notes":
        // TODO: Implement search_notes tool
        return {
          content: [
            {
              type: "text" as const,
              text: "search_notes tool not yet implemented",
            },
          ],
        };

      case "list_notes":
        // TODO: Implement list_notes tool
        return {
          content: [
            {
              type: "text" as const,
              text: "list_notes tool not yet implemented",
            },
          ],
        };

      case "get_note":
        // TODO: Implement get_note tool
        return {
          content: [
            {
              type: "text" as const,
              text: "get_note tool not yet implemented",
            },
          ],
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    throw new Error(
      `Tool execution failed: ${error instanceof Error ? error.message : String(error)}`,
    );
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Notes server running on stdio");
}

if (import.meta.main) {
  main().catch(console.error);
}
