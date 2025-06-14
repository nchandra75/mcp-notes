import { dirname, join } from "https://deno.land/std@0.208.0/path/mod.ts";
import { ensureDir, exists } from "https://deno.land/std@0.208.0/fs/mod.ts";
import { Note, NoteFrontmatter } from "./types.ts";
import { formatMarkdown, parseMarkdown } from "./markdown.ts";

export class FileManager {
  constructor(private vaultPath: string) {}

  async ensureVaultExists(): Promise<void> {
    await ensureDir(this.vaultPath);
  }

  async writeNote(filename: string, frontmatter: NoteFrontmatter, content: string): Promise<void> {
    const fullPath = join(this.vaultPath, filename);
    const dir = dirname(fullPath);

    await ensureDir(dir);

    const markdownContent = formatMarkdown(frontmatter, content);
    await Deno.writeTextFile(fullPath, markdownContent);
  }

  async readNote(filename: string): Promise<Note | null> {
    const fullPath = join(this.vaultPath, filename);

    if (!await exists(fullPath)) {
      return null;
    }

    const content = await Deno.readTextFile(fullPath);
    const { frontmatter, body } = parseMarkdown(content);

    return {
      filename,
      frontmatter,
      content: body,
      fullPath,
    };
  }

  async listNoteFiles(): Promise<string[]> {
    const files: string[] = [];

    try {
      for await (const entry of Deno.readDir(this.vaultPath)) {
        if (entry.isFile && entry.name.endsWith(".md")) {
          files.push(entry.name);
        }
      }
    } catch (error) {
      if (error instanceof Deno.errors.NotFound) {
        return [];
      }
      throw error;
    }

    return files.sort();
  }

  generateFilename(title: string): string {
    const kebabTitle = title
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");

    const date = new Date().toISOString().split("T")[0];
    return `${kebabTitle}-${date}.md`;
  }
}
