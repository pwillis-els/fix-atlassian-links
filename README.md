# About

Python script to fix (usually by search/replace) the HTTP[S] links in Atlassian products like Confluence, Jira, etc.

# Usage

## Local install/run
1. Run `pip install -e .`
2. Run `fix-atlassian-links`

## Docker install/run
1. Run `make docker-build`
2. Run `make search-replace-page`

You can pass the Confluence URL, username, and password via command-line arguments,
or via the environment variables `CONFLUENCE_URL`, `CONFLUENCE_USER`, `CONFLUENCE_PASS`.
