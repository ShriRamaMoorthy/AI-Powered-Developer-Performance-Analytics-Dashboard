# metrics_calculator.py

import pandas as pd

def calculate_metrics(commits_df, prs_df, issues_df, reviews_df):
    # Precompute developer commits data
    developer_commits = commits_df.groupby('author').size().reset_index(name='commits')

    # Commit Frequency
    commit_frequency = commits_df.groupby(commits_df['date'].dt.date).size().reset_index(name='commits')

    # PR Merge Rate
    merged_prs = prs_df[prs_df['merged_at'].notnull()]
    merge_rate = len(merged_prs) / len(prs_df) * 100

    # Issue Resolution Time
    issues_df['resolution_time'] = (issues_df['closed_at'] - issues_df['created_at']).dt.days
    avg_resolution_time = issues_df['resolution_time'].mean()

    return developer_commits, commit_frequency, merge_rate, avg_resolution_time
