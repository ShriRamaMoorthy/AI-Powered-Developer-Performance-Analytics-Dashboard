# keyword_response_generator.py

import plotly.express as px
import pandas as pd

def generate_response(query, fig1, merge_rate, avg_resolution_time, reviews_df, prs_df, issues_df, commits_df):
    response = {}
    if "commit frequency" in query.lower():
        response['chart'] = fig1

    elif "merge rate" in query.lower():
        response['metric'] = {"label": "Pull Request Merge Rate", "value": f"{merge_rate:.2f}%"}

    elif "issue resolution time" in query.lower():
        response['metric'] = {"label": "Average Issue Resolution Time", "value": f"{avg_resolution_time:.2f} days"}

    elif "review participation" in query.lower():
        review_count = reviews_df.groupby('reviewer').size().reset_index(name='total_reviews')
        response['chart'] = px.bar(review_count, x='reviewer', y='total_reviews', title='Code Review Participation')

    elif "review approval rate" in query.lower():
        total_reviews = reviews_df.groupby('reviewer').size().reset_index(name='total_reviews')
        approved_reviews = reviews_df[reviews_df['state'] == 'APPROVED'].groupby('reviewer').size().reset_index(name='approved_reviews')
        review_approval_rate = pd.merge(total_reviews, approved_reviews, on='reviewer', how='left').fillna(0)
        review_approval_rate['approval_rate'] = review_approval_rate['approved_reviews'] / review_approval_rate['total_reviews']
        response['chart'] = px.bar(review_approval_rate, x='reviewer', y='approval_rate', title='Review Approval Rate')

    elif "pr merge time" in query.lower():
        merged_prs = prs_df[prs_df['merged_at'].notnull()]
        merged_prs['created_at'] = pd.to_datetime(merged_prs['created_at'])
        merged_prs['merged_at'] = pd.to_datetime(merged_prs['merged_at'])
        merged_prs['time_to_merge'] = (merged_prs['merged_at'] - merged_prs['created_at']).dt.total_seconds() / 3600
        avg_time_to_merge = merged_prs.groupby('author')['time_to_merge'].mean().reset_index()
        response['chart'] = px.bar(avg_time_to_merge, x='author', y='time_to_merge', title='Average Time to Merge PRs (hours)')

    elif "open to close ratio" in query.lower():
        open_issues = issues_df[issues_df['closed_at'].isnull()].groupby('author').size().reset_index(name='open_issues')
        closed_issues = issues_df[issues_df['closed_at'].notnull()].groupby('author').size().reset_index(name='closed_issues')
        issue_ratio = pd.merge(open_issues, closed_issues, on='author', how='left').fillna(0)
        issue_ratio['open_to_close_ratio'] = issue_ratio['open_issues'] / issue_ratio['closed_issues']
        response['chart'] = px.bar(issue_ratio, x='author', y='open_to_close_ratio', title='Open to Close Issue Ratio')

    elif "commit message length" in query.lower():
        commits_df['message_length'] = commits_df['message'].apply(len)
        response['chart'] = px.box(commits_df, x='author', y='message_length', title='Commit Message Length Distribution')

    return response
