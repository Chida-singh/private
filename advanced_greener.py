import os
import random
import subprocess
from datetime import datetime, timedelta


def run_git_command(cmd, repo_path, env=None):
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        env=env or os.environ.copy(),
        text=True,
        capture_output=True,
        check=True
    )
    return result.stdout.strip()


def get_random_commit_message():
    messages = [
        "Fix minor bug",
        "Update README",
        "Refactor logic for clarity",
        "Improve performance of loop",
        "Add logging",
        "Tweak styling in output",
        "Fix typo",
        "Update dependencies",
        "Add comments for readability",
        "Remove unused import",
        "Reorganize folder structure",
        "Add test case",
        "Fix issue with edge case",
        "Update documentation",
        "Make function more robust",
        "Improve error handling",
        "Cleanup code",
        "Add missing check",
        "Refactor variable names",
        "Initial commit (again?)"
    ]
    return random.choice(messages)


def clone_or_use_existing(repo_url, base_dir="cloned_repos"):
    os.makedirs(base_dir, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = os.path.join(base_dir, repo_name)

    if os.path.exists(local_path):
        print(f"✅ Using existing local repo: {local_path}")
    else:
        print(f"📥 Cloning {repo_url}...")
        run_git_command(["git", "clone", repo_url], base_dir)

    return local_path


def make_commit(repo_path, date, filename="devlog.txt", message=None):
    if message is None:
        message = get_random_commit_message()

    filepath = os.path.join(repo_path, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "a") as f:
        f.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    run_git_command(["git", "add", filename], repo_path)

    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    run_git_command(["git", "commit", "-m", message], repo_path, env=env)


def push_repo(repo_path):
    try:
        run_git_command(["git", "push"], repo_path)
        print(f"✅ Pushed: {os.path.basename(repo_path)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Push failed in {repo_path}: {e.stderr.strip()}")


def random_date_in_last_year():
    today = datetime.now()
    start = today - timedelta(days=365)
    return start + timedelta(
        days=random.randint(0, 364),
        seconds=random.randint(0, 23 * 3600 + 3599)
    )


def distribute_commits_across_repos(commits, repos):
    return [random.choice(repos) for _ in range(commits)]


# CLI Wrapping
def get_repos():
    print("\n📦 Enter your public Git repository HTTPS or SSH links one by one.")
    print("Press Enter on an empty line to finish.")
    repos = []
    while True:
        repo = input("Repo URL: ").strip()
        if repo == "":
            break
        repos.append(repo)
    return repos


def get_commit_count():
    while True:
        try:
            num = input("\n🔢 How many total commits? (default: 20): ").strip()
            return 20 if not num else max(1, int(num))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def main():
    print("=" * 60)
    print("🌿 Legit Graph Greener - GitHub Contribution Booster")
    print("=" * 60)

    repos = get_repos()
    if not repos:
        print("❌ No repositories entered. Exiting.")
        return

    total_commits = get_commit_count()
    print(f"\n🛠 Generating {total_commits} commits across {len(repos)} repo(s)...\n")

    local_paths = [clone_or_use_existing(url) for url in repos]
    commit_targets = distribute_commits_across_repos(total_commits, local_paths)

    for i, repo_path in enumerate(commit_targets, 1):
        commit_time = random_date_in_last_year()
        print(f"[{i}/{total_commits}] ➤ {os.path.basename(repo_path)} @ {commit_time}")
        try:
            make_commit(repo_path, commit_time)
        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e.stderr.strip()}")

    print("\n🚀 Pushing all repositories...\n")
    for repo_path in set(commit_targets):
        push_repo(repo_path)

    print("\n✅ Done! Refresh your GitHub profile in a few minutes to see the new green squares.")


if __name__ == "__main__":
    main()
