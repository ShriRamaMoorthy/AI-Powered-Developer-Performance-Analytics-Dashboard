# github_api.py

from github import Github

def fetch_repository_data(repo_url, token):
    repo_name = repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1]
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Fetch commits
    commits = repo.get_commits()
    commits_data = []
    for commit in commits:
        author_login = commit.author.login if commit.author else 'Unknown'
        commits_data.append({
            'sha': commit.sha,
            'author': author_login,
            'date': commit.commit.author.date,
            'message': commit.commit.message
        })
    
    # Fetch PRs
    prs = repo.get_pulls(state='all')
    prs_data = [{'id': pr.id, 'author': pr.user.login, 'state': pr.state, 'created_at': pr.created_at, 'merged_at': pr.merged_at, 'title': pr.title} for pr in prs]
    
    # Fetch Issues
    issues = repo.get_issues(state='all')
    issues_data = [{'id': issue.id, 'author': issue.user.login, 'state': issue.state, 'created_at': issue.created_at, 'closed_at': issue.closed_at, 'title': issue.title} for issue in issues]
    
    # Fetch Reviews
    reviews_data = []
    for pr in prs:
        reviews = pr.get_reviews()
        for review in reviews:
            reviews_data.append({'pr_id': pr.id, 'reviewer': review.user.login, 'state': review.state, 'submitted_at': review.submitted_at})
    
    return commits_data, prs_data, issues_data, reviews_data
