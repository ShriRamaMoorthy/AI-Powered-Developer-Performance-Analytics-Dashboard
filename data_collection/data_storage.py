import os
import pandas as pd

def save_data_to_csv(commits_df, prs_df, issues_df, reviews_df, repo_name):
    # Define the directory name and path
    base_dir = 'github_data'
    repo_dir = os.path.join(base_dir, repo_name)

    # Create the directory if it doesn't exist
    os.makedirs(repo_dir, exist_ok=True)

    # Define file paths
    commits_file = os.path.join(repo_dir, 'commits.csv')
    prs_file = os.path.join(repo_dir, 'pull_requests.csv')
    issues_file = os.path.join(repo_dir, 'issues.csv')
    reviews_file = os.path.join(repo_dir, 'reviews.csv')

    # Save DataFrames to CSV
    commits_df.to_csv(commits_file, index=False)
    prs_df.to_csv(prs_file, index=False)
    issues_df.to_csv(issues_file, index=False)
    reviews_df.to_csv(reviews_file, index=False)

    return repo_dir
