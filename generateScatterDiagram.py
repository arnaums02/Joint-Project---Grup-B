import os
from github import Github
import matplotlib.pyplot as plt

# This code generates a scatter diagram with all the
# commits of the repository, showing the added lines and
# the modified files. It has to be executed manually
# using the "scatterGeneralReportGenerator.yml" workflow


token = os.getenv('GITHUB_TOKEN')
repo_name = "arnaums02/Joint-Project---Grup-B"

g = Github(token)
repo = g.get_repo(repo_name)

lines_added_per_commit = []
files_modified_per_commit = []
authors_of_commits = []

# Modify author names and colors for your repository
author_colors = {
    "arnaums02": "blue",
    "quimsb03": "green",
    "GiovanniMaerean": "red",
    "albertm15": "purple",
    "PauBarahona22": "orange"
}


def main() -> None:
    get_data()
    generate_diagram()


def get_data() -> None:
    """Gets all the lines added and files modified per commit"""
    commits = repo.get_commits()

    for commit in commits:
        lines_added = commit.stats.additions
        files_modified = len(commit.files)
        author_name = commit.author.login

        lines_added_per_commit.append(lines_added)
        files_modified_per_commit.append(files_modified)
        authors_of_commits.append(author_name)


def generate_diagram() -> None:
    """Generates and saves the scatter diagram with all the data"""
    plt.figure(figsize=(10, 6))
    legend_authors = set()
    for author, lines_added, files_modified in zip(authors_of_commits, lines_added_per_commit,
                                                   files_modified_per_commit):
        color = author_colors.get(author, "black")  # Default to black if author not in author_colors

        if author not in legend_authors:

            plt.scatter(lines_added, files_modified, color=color, label=author)
            legend_authors.add(author)
        else:
            plt.scatter(lines_added, files_modified, color=color)

    plt.xlabel('Lines added')
    plt.ylabel('Files modified')
    plt.title('Scatter Diagram of Lines added and Files modified')
    plt.legend()
    plt.grid(True)

    plt.savefig("scatter_diagram_commits.png")


if __name__ == '__main__':
    main()
