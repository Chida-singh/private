import os
import random
import subprocess
from datetime import datetime, timedelta

def get_repos():
    print("\n📦 Enter your public git repository HTTPS or SSH links one by one.")
    print("When you're done, just press Enter on an empty line.")
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
            num = input("\n🔢 How many total commits do you want to make? (default: 20): ").strip()
            if num == "":
                return 20
            num = int(num)
            if num > 0:
                return num
            else:
                print("❌ Please enter a positive number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def clone_or_use_existing(repo_url, base_dir="cloned_repos"):
    os.makedirs(base_dir, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = os.path.join(base_dir, repo_name)

    if os.path.exists(local_path):
        print(f"✅ Using existing local repo: {local_path}")
    else:
        print(f"📥 Cloning {repo_url}...")
        subprocess.run(["git", "clone", repo_url], cwd=base_dir)
    return local_path

def random_date_in_last_year():
    today = datetime.now()
    start_date = today - timedelta(days=365)
    random_days = random.randint(0, 364)
    random_seconds = random.randint(0, 23*3600 + 3599)
    commit_date = start_date + timedelta(days=random_days, seconds=random_seconds)
    return commit_date

def make_commit(date, repo_path, filename="devlog.txt", message="🟩 Legit commit via graph-greener"):
    filepath = os.path.join(repo_path, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Make meaningful-ish change
    with open(filepath, "a") as f:
        f.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')} - Auto update\n")

    subprocess.run(["git", "add", filename], cwd=repo_path)

    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def push_repo(repo_path):
    subprocess.run(["git", "push"], cwd=repo_path)

def main():
    print("=" * 60)
    print("🌿 Legit Graph Greener - Multiple Git Repo Commits Tool 🌿")
    print("=" * 60)

    repo_links = get_repos()
    if not repo_links:
        print("❌ No repositories entered. Exiting.")
        return

    total_commits = get_commit_count()
    print(f"\n🛠 Preparing to make {total_commits} commits across {len(repo_links)} repos...\n")

    local_repos = [clone_or_use_existing(link) for link in repo_links]

    for i in range(total_commits):
        chosen_repo = random.choice(local_repos)
        commit_date = random_date_in_last_year()
        print(f"[{i+1}/{total_commits}] ➤ Commit at {commit_date.strftime('%Y-%m-%d %H:%M:%S')} in {os.path.basename(chosen_repo)}")
        make_commit(commit_date, chosen_repo)

    print("\n🚀 Pushing all repositories...\n")
    for repo in local_repos:
        print(f"🔼 Pushing: {os.path.basename(repo)}")
        push_repo(repo)

    print("\n✅ Done! Your GitHub contribution graph should update shortly.")

if __name__ == "__main__":
    main()
