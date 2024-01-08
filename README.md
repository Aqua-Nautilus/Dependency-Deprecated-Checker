# Dependency Deprecation Checker

## Description

This program is a Dependency Deprecation Checker that helps to identify deprecated dependencies in your Node.js project by analyzing the `package.json` file. It checks both direct and indirect dependencies against several criteria: 
* if they are marked as deprecated on npm
* if their repository on GitHub is archived
* if the GitHub repository provided is not accessible (returns 404)
* if they do not have repository information.
  
The criteria for a deprecated package can be modified by the users.

This tool is a Proof of Concept (PoC) and does not offer a comprehensive check.

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
python scan_dependencies.py --github_token YOUR_GITHUB_TOKEN [--exclude-archived] [--exclude-repo] [--exclude-inaccessible] [package_json_file]
```

### Command-line Arguments

- `package_json_file`: Path to `package.json` file. Defaults to 'package.json' in the current directory.
- `--github-token`: GitHub token for API access. This is mandatory unless `--exclude-archived` is used.
- `--exclude-archived`: Exclude alerting on packages linked to archived repositories in GitHub.
- `--exclude-repo`: Exclude alerting on packages without an associated repository.
- `--exclude-inaccessible`: Exclude alerting on packages with a GitHub repository that is not accessible (404).


An example of the results on the sample package.json:

![sample_package_json_run](https://github.com/Ilaygoldman/dependency_deprecated/assets/29836366/0a5ccb39-0619-47e8-89ec-aeb66825f6b0)
