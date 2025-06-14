export class Settings {
  static getVaultPath(): string {
    const vaultPath = Deno.env.get("OBSIDIAN_VAULT_PATH");
    if (!vaultPath) {
      throw new Error("OBSIDIAN_VAULT_PATH environment variable is required");
    }
    return vaultPath;
  }

  static getGitCommitTemplate(): string {
    return Deno.env.get("GIT_COMMIT_TEMPLATE") || "Add note: {title}";
  }

  static isGitEnabled(): boolean {
    return Deno.env.get("DISABLE_GIT") !== "true";
  }
}
