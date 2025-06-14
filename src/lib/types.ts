export interface NoteFrontmatter {
  created: string;
  updated: string;
  conversation_id?: string;
  tags: string[];
  ai_client?: string;
  summary: string;
}

export interface Note {
  filename: string;
  frontmatter: NoteFrontmatter;
  content: string;
  fullPath: string;
}

export interface SearchResult {
  note: Note;
  score: number;
  matches: string[];
}

export interface CreateNoteParams {
  title: string;
  content: string;
  tags?: string[];
  conversation_id?: string;
  ai_client?: string;
  summary?: string;
}

export interface SearchNotesParams {
  query: string;
  tags?: string[];
  limit?: number;
}

export interface ListNotesParams {
  tags?: string[];
  limit?: number;
  sort?: "created" | "updated" | "title";
  order?: "asc" | "desc";
}

export interface McpToolResult {
  content: Array<{
    type: "text";
    text: string;
  }>;
}

export interface McpError {
  code: number;
  message: string;
  data?: unknown;
}
