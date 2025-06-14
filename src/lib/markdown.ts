import { NoteFrontmatter } from "./types.ts";

// Manual YAML creation to avoid the undefined value issue
function manualYamlStringify(obj: Record<string, any>): string {
  const lines: string[] = [];
  
  for (const [key, value] of Object.entries(obj)) {
    if (value === undefined || value === null) continue;
    
    if (Array.isArray(value)) {
      if (value.length === 0) {
        lines.push(`${key}: []`);
      } else {
        lines.push(`${key}:`);
        for (const item of value) {
          lines.push(`  - ${item}`);
        }
      }
    } else if (typeof value === 'string') {
      // Handle strings that might need quoting
      if (value.includes(':') || value.includes('#') || value.includes('\n')) {
        lines.push(`${key}: "${value.replace(/"/g, '\\"')}"`); 
      } else {
        lines.push(`${key}: ${value}`);
      }
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  
  return lines.join('\n');
}

// Simple YAML parser for frontmatter (basic implementation)
function manualYamlParse(yamlString: string): Record<string, any> {
  const result: Record<string, any> = {};
  const lines = yamlString.split('\n').filter(line => line.trim());
  
  let currentKey = '';
  let inArray = false;
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    
    if (trimmed.startsWith('- ')) {
      // Array item
      if (currentKey && inArray) {
        if (!Array.isArray(result[currentKey])) {
          result[currentKey] = [];
        }
        result[currentKey].push(trimmed.substring(2));
      }
    } else if (trimmed.includes(':')) {
      // Key-value pair
      const [key, ...valueParts] = trimmed.split(':');
      const value = valueParts.join(':').trim();
      currentKey = key.trim();
      inArray = false;
      
      if (value === '[]') {
        result[currentKey] = [];
      } else if (value === '') {
        // Might be start of array
        inArray = true;
        result[currentKey] = [];
      } else {
        // Remove quotes if present
        const cleanValue = value.replace(/^["']|["']$/g, '');
        result[currentKey] = cleanValue;
      }
    }
  }
  
  return result;
}

// Use manual YAML functions
const stringify = manualYamlStringify;
const parse = manualYamlParse;

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
  // The manual stringify function already filters out undefined/null values
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

  // Create base frontmatter with only defined values
  const frontmatter: NoteFrontmatter = {
    created: now,
    updated: now,
    tags: tags || [],
    summary: summary || `Note about ${title}`,
  };

  // Only add optional fields if they have non-empty values
  if (conversationId && conversationId.trim() !== '') {
    frontmatter.conversation_id = conversationId;
  }
  if (aiClient && aiClient.trim() !== '') {
    frontmatter.ai_client = aiClient;
  }

  return frontmatter;
}
