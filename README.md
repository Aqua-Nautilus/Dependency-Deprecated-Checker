# Dependency Deprecation Checker

## Description

This program is a Dependency Deprecation Checker that helps to identify deprecated dependencies in your Node.js project by analyzing the `package.json` file. It checks both direct and indirect dependencies against several criteria: if they are marked as deprecated on npm, if they do not have repository information, or if their repository on GitHub is archived.

## Features

- **Deep Scanning**: Analyzes both direct and indirect dependencies for deprecation.
- **Customizable Criteria**: Allows users to define what constitutes a deprecated package.
- **GitHub Integration**: Can utilize a GitHub token to check the archival status of repositories.

## Installation

Before you begin, ensure you have Python installed on your system. Then, clone the repository and install the dependencies:

```bash
git clone https://github.com/Aqua-Nautilus/Dependency-Deprecated-Checker.git
cd Dependency-Deprecated-Checker
pip install -r requirements.txt
```

## Usage

To use the Dependency Deprecation Checker, you will need a GitHub token (without permissions).

```bash
python scan_dependencies.py --github_token YOUR_GITHUB_TOKEN [--exclude-archived] [--exclude-repo]
```

### Command-line Arguments

- `package_json_file`: Path to `package.json` file. Defaults to 'package.json' in the current directory.
- `--github-token`: GitHub token for API access. This is mandatory unless `--exclude-archived` is used.
- `--exclude-archived`: Exclude checking if a GitHub repository is archived.
- `--exclude-repo`: Exclude alerting on packages without an associated repository.


An example of the results on the sample package.json: