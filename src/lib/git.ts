export class GitManager {
  constructor(private vaultPath: string) {}

  async commitNote(filename: string, title: string): Promise<string> {
    try {
      // Add the specific file
      const addProcess = new Deno.Command("git", {
        args: ["add", filename],
        cwd: this.vaultPath,
      });
      await addProcess.output();

      // Create commit message
      const template = Deno.env.get("GIT_COMMIT_TEMPLATE") || "Add note: %TITLE%";
      const commitMessage = template.replace("%TITLE%", title);

      // Commit the file
      const commitProcess = new Deno.Command("git", {
        args: ["commit", "-m", commitMessage],
        cwd: this.vaultPath,
      });
      const commitResult = await commitProcess.output();

      if (commitResult.success) {
        // Get the commit hash
        const hashProcess = new Deno.Command("git", {
          args: ["rev-parse", "HEAD"],
          cwd: this.vaultPath,
        });
        const hashResult = await hashProcess.output();

        if (hashResult.success) {
          return new TextDecoder().decode(hashResult.stdout).trim();
        }
      }

      return "commit_created";
    } catch (error) {
      console.error("Git commit failed:", error);
      return "commit_failed";
    }
  }

  async isGitRepo(): Promise<boolean> {
    try {
      const process = new Deno.Command("git", {
        args: ["rev-parse", "--git-dir"],
        cwd: this.vaultPath,
      });
      const result = await process.output();
      return result.success;
    } catch {
      return false;
    }
  }
}
