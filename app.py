import streamlit as st
import pandas as pd
import plotly.express as px
from data_collection.github_api import fetch_repository_data
from data_collection.data_storage import save_data_to_csv
from metrics.metrics_calculator import calculate_metrics
from visualization.dashboard import create_visualizations
from query_interface.keyword_response_generator import generate_response
import re

# import os
# github_token = os.getenv("GITHUB_TOKEN")

# token='KEY'

def extract_repo_name(url):
    """Extract repository name from URL."""
    # Extract the part of the URL after the last slash
    return url.rstrip('/').split('/')[-1]

def sanitize_filename(filename):
    """Sanitize the filename to ensure it's valid."""
    return re.sub(r'[\/:*?"<>|]', '', filename)

@st.cache_data
def load_data_from_repo(repo_url, token):
    commits_data, prs_data, issues_data, reviews_data = fetch_repository_data(repo_url, token)
    return (pd.DataFrame(commits_data), pd.DataFrame(prs_data), pd.DataFrame(issues_data), pd.DataFrame(reviews_data))

@st.cache_data
def save_and_return_datasets(repo_url, commits_df, prs_df, issues_df, reviews_df):
    repo_name = extract_repo_name(repo_url)
    sanitized_repo_name = sanitize_filename(repo_name)
    output_dir = save_data_to_csv(commits_df, prs_df, issues_df, reviews_df, repo_name=sanitized_repo_name)
    return output_dir

# Use a session state to store repository URLs and selected repository
if 'repo_data' not in st.session_state:
    st.session_state.repo_data = {}
if 'repo_list' not in st.session_state:
    st.session_state.repo_list = []

# Streamlit UI
st.title("Developer Performance Analytics Dashboard")

repo_url = st.text_input("Enter the GitHub repository URL:")

if st.button("Add Repository"):
    if repo_url and repo_url not in st.session_state.repo_list:
        st.session_state.repo_list.append(repo_url)
        st.write(f"Repository URL '{repo_url}' added.")
    elif repo_url in st.session_state.repo_list:
        st.write("Repository URL already added.")
    else:
        st.write("Please enter a valid repository URL.")

if st.session_state.repo_list:
    st.write("Repositories Added:")
    for url in st.session_state.repo_list:
        st.write(url)

    selected_repo = st.selectbox("Select a repository for analysis:", options=st.session_state.repo_list)

    if selected_repo:
        if selected_repo not in st.session_state.repo_data:
            with st.spinner('Fetching and processing data from the repository...'):
                commits_df, prs_df, issues_df, reviews_df = load_data_from_repo(selected_repo, token)
                output_dir = save_and_return_datasets(selected_repo, commits_df, prs_df, issues_df, reviews_df)
                st.session_state.repo_data[selected_repo] = {
                    'commits': commits_df,
                    'prs': prs_df,
                    'issues': issues_df,
                    'reviews': reviews_df
                }
                st.success("Data fetching and processing complete.")
                st.write("Datasets have been saved to the folder:", output_dir)
        else:
            st.write("Data for this repository is already loaded.")

        data = st.session_state.repo_data[selected_repo]
        commits_df = data['commits']
        prs_df = data['prs']
        issues_df = data['issues']
        reviews_df = data['reviews']

        # Calculate metrics
        developer_commits, commit_frequency, merge_rate, avg_resolution_time = calculate_metrics(commits_df, prs_df, issues_df, reviews_df)
        fig1, fig2, fig3, fig4, fig5, fig6 = create_visualizations(commit_frequency, developer_commits, prs_df, issues_df, reviews_df, commits_df)

        # Navigation
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", ["Overall Metrics", "Individual Developer Statistics", "Natural Language Query Interface", "View Datasets"])

        if selection == "Overall Metrics":
            st.subheader("Overall Repository Metrics")
            st.plotly_chart(fig1)
            st.metric(label="Pull Request Merge Rate", value=f"{merge_rate:.2f}%")
            st.metric(label="Average Issue Resolution Time", value=f"{avg_resolution_time:.2f} days")
            st.header('Code Review Participation')
            st.plotly_chart(fig2)
            st.header('Review Approval Rate')
            st.plotly_chart(fig3)
            st.header('Average Time to Merge PRs')
            st.plotly_chart(fig4)
            st.header('Open to Close Issue Ratio')
            st.plotly_chart(fig5)
            st.header('Commit Message Length')
            st.plotly_chart(fig6)

        elif selection == "Individual Developer Statistics":
            st.subheader("Individual Developer Statistics")
            selected_dev = st.selectbox("Select Developer", developer_commits['author'])
            dev_commits = commits_df[commits_df['author'] == selected_dev].groupby(commits_df['date'].dt.date).size().reset_index(name='commits')
            fig_dev_commit = px.line(dev_commits, x='date', y='commits', title=f'Commit Frequency for {selected_dev}')
            st.plotly_chart(fig_dev_commit)

            dev_prs = prs_df[prs_df['author'] == selected_dev]
            total_dev_prs = len(dev_prs)
            merged_dev_prs = len(dev_prs[prs_df['state'] == 'merged'])
            dev_pr_merge_rate = (merged_dev_prs / total_dev_prs) * 100 if total_dev_prs != 0 else 0
            st.metric(label=f"PR Merge Rate for {selected_dev}", value=f"{dev_pr_merge_rate:.2f}%")

            dev_issues = issues_df[issues_df['author'] == selected_dev]
            if not dev_issues.empty:
                dev_issues['resolution_time'] = (dev_issues['closed_at'] - dev_issues['created_at']).dt.days
                avg_dev_resolution_time = dev_issues['resolution_time'].mean()
                st.metric(label=f"Avg Issue Resolution Time for {selected_dev}", value=f"{avg_dev_resolution_time:.2f} days")
            else:
                st.write(f"No issues found for {selected_dev}")

            st.plotly_chart(px.bar(developer_commits, x='author', y='commits', title='Commits by Developer'))

        elif selection == "Natural Language Query Interface":
            st.subheader("Natural Language Query Interface")
            query = st.text_input("Ask a question:")
            if query:
                response = generate_response(query, fig1, merge_rate, avg_resolution_time, reviews_df, prs_df, issues_df, commits_df)
                if 'chart' in response:
                    st.plotly_chart(response['chart'])
                if 'metric' in response:
                    st.metric(label=response['metric']['label'], value=response['metric']['value'])

        elif selection == "View Datasets":
            st.subheader("View Datasets")
            dataset_selection = st.selectbox("Select a dataset to view:", ["Commits", "Pull Requests", "Issues", "Code Reviews"])
            if dataset_selection == "Commits":
                st.write("Displaying the first few rows of Commits dataset:")
                st.write(commits_df.head())
            elif dataset_selection == "Pull Requests":
                st.write("Displaying the first few rows of Pull Requests dataset:")
                st.write(prs_df.head())
            elif dataset_selection == "Issues":
                st.write("Displaying the first few rows of Issues dataset:")
                st.write(issues_df.head())
            elif dataset_selection == "Code Reviews":
                st.write("Displaying the first few rows of Code Reviews dataset:")
                st.write(reviews_df.head())
else:
    st.write("No repositories added yet. Please enter a repository URL and click 'Add Repository'.")
