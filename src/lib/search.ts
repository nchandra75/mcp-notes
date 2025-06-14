import { Note, SearchResult } from "./types.ts";

export class SearchEngine {
  searchNotes(notes: Note[], query: string, tagFilter?: string[]): SearchResult[] {
    const results: SearchResult[] = [];
    const queryLower = query.toLowerCase();

    for (const note of notes) {
      // Tag filtering
      if (tagFilter && tagFilter.length > 0) {
        const hasMatchingTag = tagFilter.some((tag) => note.frontmatter.tags.includes(tag));
        if (!hasMatchingTag) continue;
      }

      // Calculate relevance score
      let score = 0;
      const matches: string[] = [];

      // Title match (highest weight)
      const titleMatch = this.calculateMatch(note.filename, queryLower);
      if (titleMatch.score > 0) {
        score += titleMatch.score * 3;
        matches.push(`Title: ${titleMatch.text}`);
      }

      // Summary match (high weight)
      const summaryMatch = this.calculateMatch(note.frontmatter.summary, queryLower);
      if (summaryMatch.score > 0) {
        score += summaryMatch.score * 2;
        matches.push(`Summary: ${summaryMatch.text}`);
      }

      // Content match (medium weight)
      const contentMatch = this.calculateMatch(note.content, queryLower);
      if (contentMatch.score > 0) {
        score += contentMatch.score;
        matches.push(`Content: ${contentMatch.text}`);
      }

      // Tag match (medium weight)
      const tagMatches = note.frontmatter.tags.filter((tag) =>
        tag.toLowerCase().includes(queryLower)
      );
      if (tagMatches.length > 0) {
        score += tagMatches.length * 1.5;
        matches.push(`Tags: ${tagMatches.join(", ")}`);
      }

      if (score > 0) {
        results.push({
          note,
          score,
          matches,
        });
      }
    }

    // Sort by score (descending)
    return results.sort((a, b) => b.score - a.score);
  }

  private calculateMatch(text: string, query: string): { score: number; text: string } {
    if (!text) return { score: 0, text: "" };

    const textLower = text.toLowerCase();

    // Exact match
    if (textLower === query) {
      return { score: 10, text: text };
    }

    // Contains query
    if (textLower.includes(query)) {
      const index = textLower.indexOf(query);
      const contextStart = Math.max(0, index - 30);
      const contextEnd = Math.min(text.length, index + query.length + 30);
      const context = text.substring(contextStart, contextEnd);

      return {
        score: 5,
        text: contextStart > 0
          ? "..." + context
          : context + (contextEnd < text.length ? "..." : ""),
      };
    }

    // Word match
    const words = query.split(/\s+/);
    const matchingWords = words.filter((word) => textLower.includes(word));

    if (matchingWords.length > 0) {
      const score = (matchingWords.length / words.length) * 2;
      return { score, text: text.substring(0, 100) + (text.length > 100 ? "..." : "") };
    }

    return { score: 0, text: "" };
  }
}
