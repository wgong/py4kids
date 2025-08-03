from prefect import flow, task
import httpx

def cleanup_repo(repo: str, tags: list[str] = ["https://github.com/"]):
    for tag in tags:
        if tag in repo:
            repo = repo.replace(tag, "")
    return repo

@task
def get_repos():
    repos = [
        "PrefectHQ/Prefect", 
        "prefecthq/prefect-aws", 
        "https://github.com/The-Pocket/PocketFlow",
        "https://github.com/digital-duck/data-copilot",
        "https://github.com/wgong/py4kids",
        "https://github.com/sethdford/flowx",
        "https://github.com/ruvnet/claude-flow",
        "",
    ]
    return [cleanup_repo(repo.strip()) for repo in repos if repo.strip()]

@task(log_prints=True)
def get_stars(repo: str):
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    print(f"{repo} has {count} stars!")
    return {'repo': repo, 'stars': count}

@flow(name="Main Flow")
def main():
    repos = get_repos()
    results = get_stars.map(repos)
    actual_results = [future.result() for future in results]
    return actual_results

# run the flow!
if __name__ == "__main__":
    flow_result = main()
    print("Flow executed successfully!\nResults:", flow_result)
