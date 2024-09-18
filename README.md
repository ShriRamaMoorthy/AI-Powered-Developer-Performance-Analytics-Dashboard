# AI-Powered Developer Performance Analytics Dashboard
---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Data Sources](#data-sources)
5. [Installation](#installation)
6. [Interact with the Dashboard](#interact-with-the-dashboard)
7. [Usage Guide](#usage-guide)
8. [Future Improvements](#future-improvements)
9. [Project Structure](#project-structure)



## 1. Project Overview

The **AI-Powered Developer Performance Analytics Dashboard** is an interactive web application built with Streamlit for the construction, visualization, and analysis of key metrics associated with any GitHub repository. Users can go on to analyze, interpret, or view various performance metrics such as how often one commits, pull request merge rates, and issue resolution times among others. It also permits natural language queries to access specific insights directly.


## 2. Features

- **Repository Data Management**: Add and manage multiple GitHub repositories, with data being fetched and saved locally.
- **Visualizations**: Interactive charts and graphs to display repository metrics such as commit frequency, PR merge rates, and more.
- **Natural Language Query Interface**: Query the dashboard using natural language to get insights into repository data.
- **Individual Developer Statistics**: View performance metrics for individual developers, including commit frequency and PR merge rates.


## 3. Technologies Used
The AI-Powered Developer Performance Analytics Dashboard delivers a silky-smooth experience through modern libraries and technologies. Here is the outline of the key technologies used for this project:

* Python: Being the overall core programming language used for the project, thanks to its simplicity and vast ecosystem of libraries.
* Streamlit: This is a Python framework for building web applications. It is used to build this dashboard interface.
* Plotly: A graphing library that's used for creating interactive charts and visualizations directly in the dashboard.
* Pandas: This library was used for data manipulation, and importantly it was mainly applied for processing fetched GitHub repository data and for the calculation of different types of metrics.
* GitHub REST API: This is the main source of data for fetching of repository related data such as commits, pull requests issues and code reviews.


## 4. Data Sources
The AI-Powered Developer Performance Analytics Dashboard collects real-time data from GitHub repositories using the GitHub REST API. Below are the key data sources:

1. Commits Data: Contains information on all commits made to the repository, including the author, timestamp, and commit message.
2. Pull Requests Data: Fetches details on open, closed, and merged pull requests, along with their authors, state, and merge details.
3. Issues Data: Retrieves data on repository issues, including those created and closed, their resolution time, and status.
4. Code Reviews Data: Gathers data about code reviews, including participation, approval rates, and the time to review.

The data is fetched dynamically, processed using pandas, and used to calculate performance metrics that are visualized in the dashboard. The data is also stored locally in CSV format for future use.


## 5. Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

2. **Create and Activate a Virtual Environment** 

    ```python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**
    `pip install -r requirements.txt`

4. **Set Up Environment Variables**
`GITHUB_TOKEN=your_github_token`

5. **Run the Streamlit Application**
`streamlit run app.py`



## 6. Interact with the Dashboard
1. **Add a Repository**: Enter the GitHub repository URL in the input field and click "Add Repository" to fetch and process data.
2. **Select a Repository**: Choose a repository among all the other available repositories from the dropdown menu to view and analyze its metrics.
3. **View**: Use the sidebar to navigate between different metrics and sections
4. **Overall Metrics**: Displays general metrics for the selected repository.
5. **Individual Developer Statistics**: View performance metrics for individual developers. One can use the dropdown menu to analyze the activities of different available developers.
6. **Natural Language Query Interface**: Ask questions about the repository's data.
7. **View Datasets**: View raw data for commits, pull requests, issues, and code reviews.
Metrics
8. **The Metrics that are used as follows :**
    8.1 **Commit Frequency**: Shows the number of commits over time for the selected repository or developer.
    8.2 **Pull Request Merge Rate**: Displays the percentage of pull requests merged versus those opened.
    8.3 **Average Issue Resolution Time**: Measures the average time taken to resolve issues in the repository.
    8.4 **Code Review Participation**: Visualizes the participation in code reviews.
    8.5 **Review Approval Rate**: Shows the rate at which code reviews are approved.
    8.6 **Average Time to Merge PRs**: Displays the average time taken to merge pull requests.
    8.7 **Open to Close Issue Ratio**: Compares the number of open issues to closed issues


## 7. Usage Guide
**1. Adding Repositories**
* In the main interface, enter the GitHub repository URL in the input field.
* Click "Add Repository" to fetch and analyze data from the repository. 

**2. Viewing Repositories**
* Once repositories are added, they will be listed under "Repositories Added".
* Select any repository from the dropdown to start analyzing its performance.

**3. Navigation Options**
* The sidebar provides several navigation options for analyzing repository performance:
**Overall Metrics** : View the repository's overall activities (or) performance with interactive charts and key metrics such as PR Merge Rate and Issue Resolution Time to name a few.
**Individual Developer Statistics** : Select a developer from the dropdown to view detailed statistics on their commit frequency, PR merge rate, and issue resolution time.
**Natural Language Query Interface** : Type in a query, such as "What is the PR merge rate?" to get AI-powered responses and visualizations.
**View Datasets** : You can select a dataset (commits, PRs, issues, reviews) to view the raw data that is fetched from the GitHub repository to get a gist (or) quick understanding of the data.

**4. Analyzing Metrics**
* **PR Merge Rate:** Displays the percentage of pull requests that were merged.
* **Commit Frequency:** Shows the frequency of commits by developers over time.
* **Issue Resolution Time:** Displays the average time taken to resolve issues in the repository.
* **Review Approval Rate:** The percentage of code reviews that were approved.
* **Commit Message Length:** A visual representation of the length of commit messages for better understanding of commit quality.

**5. Natural Language Query Interface**
* Ask questions about the repository in plain English, such as "What is the average resolution time?" or "How many PRs were merged?" to receive AI-generated responses along with relevant charts and metrics.
* Some of the queries that can be prompted are : 
    * "Show commit frequency for JohnDoe."
    * "Display commit frequency over the last month."
    * "What is the PR merge rate?"
    * "PR merge rate for Alice."
    * "What is the average issue resolution time?"
    * "Show issue resolution time."
    * "Code review participation statistics."
    * "Who reviewed the most code?"
    * "Average time to merge PRs."
    * "PR merge time for Alice."
    * "Show commit message length distribution."
    * "What is the average length of commit messages?"

**6. View Datasets**
* Switch between Commits, Pull Requests, Issues, and Code Reviews to view the raw data directly in the dashboard.


## 8. Future Improvements
This project can be extended with several future enhancements to improve functionality and user experience:

1. **Multi-User Support**: This Functionality can be added to enable multiple users to utilize the dashboard simultaneously with personalized views or different repositories.
2. **Integrating More Data Sources**: The dashboard shall be integrated with more sources than just Jenkins, so you can add build logs, Jira for issue tracking, or other DevOps tools to view development performance more holistically.
3. **User Authentication**: Implementing OAuth authentication for GitHub to securely fetch data from a respective user's repository.

## 9. Project Structure
```plaintext
dev_performance_dashboard/
├── data_collection/
│   ├── github_api.py               # Fetches repository data from the GitHub API
│   └── data_storage.py             # Handles saving data to CSV
├── metrics/
│   └── metrics_calculator.py       # Calculates various metrics from the data
├── visualization/
│   └── dashboard.py                # Generates visualizations using Plotly
├── query_interface/
│   └── keyword_response_generator.py # Provides response generation for natural language queries
├── app.py                          # Main Streamlit application
├── requirements.txt                # List of required Python packages
└── README.md                       # Documentation
