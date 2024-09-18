# dashboard.py

import plotly.express as px
import pandas as pd

def create_visualizations(commit_frequency, developer_commits, prs_df, issues_df, reviews_df,commits_df):
    fig1 = px.line(commit_frequency, x='date', y='commits', title='Commit Frequency Over Time')

    # Code Review Participation
    review_count = reviews_df.groupby('reviewer').size().reset_index(name='total_reviews')
    fig2 = px.bar(review_count, x='reviewer', y='total_reviews', title='Code Review Participation')

    # Review Approval Rate
    total_reviews = reviews_df.groupby('reviewer').size().reset_index(name='total_reviews')
    approved_reviews = reviews_df[reviews_df['state'] == 'APPROVED'].groupby('reviewer').size().reset_index(name='approved_reviews')
    review_approval_rate = pd.merge(total_reviews, approved_reviews, on='reviewer', how='left').fillna(0)
    review_approval_rate['approval_rate'] = review_approval_rate['approved_reviews'] / review_approval_rate['total_reviews']
    fig3 = px.bar(review_approval_rate, x='reviewer', y='approval_rate', title='Review Approval Rate')

    # PR Time to Merge
    merged_prs = prs_df[prs_df['merged_at'].notnull()]
    merged_prs['created_at'] = pd.to_datetime(merged_prs['created_at'])
    merged_prs['merged_at'] = pd.to_datetime(merged_prs['merged_at'])
    merged_prs['time_to_merge'] = (merged_prs['merged_at'] - merged_prs['created_at']).dt.total_seconds() / 3600
    avg_time_to_merge = merged_prs.groupby('author')['time_to_merge'].mean().reset_index()
    fig4 = px.bar(avg_time_to_merge, x='author', y='time_to_merge', title='Average Time to Merge PRs (hours)')

    # Issue Open to Close Ratio
    open_issues = issues_df[issues_df['closed_at'].isnull()].groupby('author').size().reset_index(name='open_issues')
    closed_issues = issues_df[issues_df['closed_at'].notnull()].groupby('author').size().reset_index(name='closed_issues')
    issue_ratio = pd.merge(open_issues, closed_issues, on='author', how='left').fillna(0)
    issue_ratio['open_to_close_ratio'] = issue_ratio['open_issues'] / issue_ratio['closed_issues']
    fig5 = px.bar(issue_ratio, x='author', y='open_to_close_ratio', title='Open to Close Issue Ratio')

    # Commit Message Length
    commits_df['message_length'] = commits_df['message'].apply(len)
    fig6 = px.box(commits_df, x='author', y='message_length', title='Commit Message Length Distribution')

    return fig1, fig2, fig3, fig4, fig5, fig6
