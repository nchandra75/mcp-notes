import { parse, stringify } from "https://deno.land/std@0.208.0/yaml/mod.ts";
import { NoteFrontmatter } from "./types.ts";

export interface ParsedMarkdown {
  frontmatter: NoteFrontmatter;
  body: string;
}

export function parseMarkdown(content: string): ParsedMarkdown {
  const lines = content.split("\n");

  if (lines[0] !== "---") {
    throw new Error("Invalid markdown format: missing frontmatter");
  }

  const frontmatterEnd = lines.findIndex((line, index) => index > 0 && line === "---");
  if (frontmatterEnd === -1) {
    throw new Error("Invalid markdown format: unclosed frontmatter");
  }

  const frontmatterContent = lines.slice(1, frontmatterEnd).join("\n");
  const body = lines.slice(frontmatterEnd + 1).join("\n").trim();

  const frontmatter = parse(frontmatterContent) as NoteFrontmatter;

  return { frontmatter, body };
}

export function formatMarkdown(frontmatter: NoteFrontmatter, content: string): string {
  const yamlContent = stringify(frontmatter).trim();

  return `---
${yamlContent}
---

${content}`;
}

export function createDefaultFrontmatter(
  title: string,
  summary?: string,
  tags: string[] = [],
  conversationId?: string,
  aiClient?: string,
): NoteFrontmatter {
  const now = new Date().toISOString();

  return {
    created: now,
    updated: now,
    conversation_id: conversationId,
    tags,
    ai_client: aiClient,
    summary: summary || `Note about ${title}`,
  };
}
