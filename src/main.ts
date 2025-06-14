#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

import { Server } from "npm:@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "npm:@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "npm:@modelcontextprotocol/sdk/types.js";

import { FileManager } from "./lib/file_manager.ts";
import { GitManager } from "./lib/git.ts";
import { SearchEngine } from "./lib/search.ts";
import { createDefaultFrontmatter } from "./lib/markdown.ts";
import { CreateNoteParams, ListNotesParams, SearchNotesParams } from "./lib/types.ts";

// Initialize managers
const vaultPath = Deno.env.get("OBSIDIAN_VAULT_PATH");
if (!vaultPath) {
  console.error("Error: OBSIDIAN_VAULT_PATH environment variable is required");
  Deno.exit(1);
}

const fileManager = new FileManager(vaultPath);
const gitManager = new GitManager(vaultPath);
const searchEngine = new SearchEngine();

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

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "create_note": {
        const params = args as unknown as CreateNoteParams;
        
        // Validate required parameters
        if (!params || typeof params !== 'object') {
          throw new Error("Invalid parameters: expected object");
        }
        if (!params.title || typeof params.title !== 'string') {
          throw new Error("Missing required parameter: title (string)");
        }
        if (!params.content || typeof params.content !== 'string') {
          throw new Error("Missing required parameter: content (string)");
        }
        
        await fileManager.ensureVaultExists();

        const filename = fileManager.generateFilename(params.title);
        const frontmatter = createDefaultFrontmatter(
          params.title,
          params.summary || `Note about ${params.title}`,
          params.tags || [],
          params.conversation_id,
          params.ai_client,
        );

        await fileManager.writeNote(filename, frontmatter, params.content);

        // Attempt git commit if repository exists
        let commitHash = "";
        if (await gitManager.isGitRepo()) {
          commitHash = await gitManager.commitNote(filename, params.title);
        }

        return {
          content: [
            {
              type: "text" as const,
              text: `Note created successfully:\n\nFilename: ${filename}\nPath: ${vaultPath}/${filename}\nGit commit: ${commitHash || "No git repository found"}\n\nThe note has been saved to your Obsidian vault and is ready to use.`,
            },
          ],
        };
      }

      case "search_notes": {
        const params = args as unknown as SearchNotesParams;
        
        // Validate required parameters
        if (!params || typeof params !== 'object') {
          throw new Error("Invalid parameters: expected object");
        }
        if (!params.query || typeof params.query !== 'string') {
          throw new Error("Missing required parameter: query (string)");
        }
        
        await fileManager.ensureVaultExists();

        const noteFiles = await fileManager.listNoteFiles();
        const notes = [];

        for (const filename of noteFiles) {
          const note = await fileManager.readNote(filename);
          if (note) {
            notes.push(note);
          }
        }

        const results = searchEngine.searchNotes(notes, params.query, params.tags);
        const limitedResults = results.slice(0, params.limit || 10);

        if (limitedResults.length === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text: `No notes found matching query: "${params.query}"`,
              },
            ],
          };
        }

        const resultText = limitedResults.map((result, index) => {
          const note = result.note;
          return `${index + 1}. **${note.filename}** (Score: ${result.score.toFixed(1)})\n` +
            `   Summary: ${note.frontmatter.summary}\n` +
            `   Tags: ${note.frontmatter.tags.join(", ")}\n` +
            `   Created: ${new Date(note.frontmatter.created).toLocaleDateString()}\n` +
            `   Matches: ${result.matches.join("; ")}\n`;
        }).join("\n");

        return {
          content: [
            {
              type: "text" as const,
              text:
                `Found ${limitedResults.length} notes matching "${params.query}":\n\n${resultText}`,
            },
          ],
        };
      }

      case "list_notes": {
        const params = (args as unknown as ListNotesParams) || {};
        await fileManager.ensureVaultExists();

        const noteFiles = await fileManager.listNoteFiles();
        const notes = [];

        for (const filename of noteFiles) {
          const note = await fileManager.readNote(filename);
          if (note) {
            // Filter by tags if specified
            if (params.tags && params.tags.length > 0) {
              const hasMatchingTag = params.tags.some((tag) => note.frontmatter.tags.includes(tag));
              if (!hasMatchingTag) continue;
            }
            notes.push(note);
          }
        }

        // Sort notes
        const sortField = params.sort || "updated";
        const sortOrder = params.order || "desc";

        notes.sort((a, b) => {
          let aValue, bValue;

          switch (sortField) {
            case "created":
              aValue = new Date(a.frontmatter.created).getTime();
              bValue = new Date(b.frontmatter.created).getTime();
              break;
            case "updated":
              aValue = new Date(a.frontmatter.updated).getTime();
              bValue = new Date(b.frontmatter.updated).getTime();
              break;
            case "title":
              aValue = a.filename.toLowerCase();
              bValue = b.filename.toLowerCase();
              break;
            default:
              aValue = new Date(a.frontmatter.updated).getTime();
              bValue = new Date(b.frontmatter.updated).getTime();
          }

          if (sortOrder === "asc") {
            return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
          } else {
            return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
          }
        });

        const limitedNotes = notes.slice(0, params.limit || 20);

        if (limitedNotes.length === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text: "No notes found in the vault.",
              },
            ],
          };
        }

        const notesList = limitedNotes.map((note, index) => {
          return `${index + 1}. **${note.filename}**\n` +
            `   Summary: ${note.frontmatter.summary}\n` +
            `   Tags: ${note.frontmatter.tags.join(", ")}\n` +
            `   Created: ${new Date(note.frontmatter.created).toLocaleDateString()}\n` +
            `   Updated: ${new Date(note.frontmatter.updated).toLocaleDateString()}\n`;
        }).join("\n");

        return {
          content: [
            {
              type: "text" as const,
              text: `Found ${limitedNotes.length} notes in your vault:\n\n${notesList}`,
            },
          ],
        };
      }

      case "get_note": {
        const params = args as unknown as { filename: string };
        
        // Validate required parameters
        if (!params || typeof params !== 'object') {
          throw new Error("Invalid parameters: expected object");
        }
        if (!params.filename || typeof params.filename !== 'string') {
          throw new Error("Missing required parameter: filename (string)");
        }
        
        await fileManager.ensureVaultExists();

        const note = await fileManager.readNote(params.filename);

        if (!note) {
          return {
            content: [
              {
                type: "text" as const,
                text:
                  `Note not found: ${params.filename}\n\nMake sure the filename is correct and the note exists in your vault.`,
              },
            ],
          };
        }

        const frontmatterText = Object.entries(note.frontmatter)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(", ") : value}`)
          .join("\n");

        return {
          content: [
            {
              type: "text" as const,
              text:
                `**${note.filename}**\n\n**Frontmatter:**\n${frontmatterText}\n\n**Content:**\n${note.content}`,
            },
          ],
        };
      }

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
