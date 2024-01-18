# Dependency Deprecation Checker

## Description

This program is a Dependency Deprecation Checker that helps to identify deprecated dependencies in your Node.js project by analyzing the `package.json` file. It checks both direct and indirect dependencies against several criteria: 
* if they are marked as deprecated on npm
* if their repository on GitHub is archived
* if the GitHub repository provided is not accessible (returns 404)
* if they do not have repository information.
  
The criteria for a deprecated package can be modified by the users.

This tool is a Proof of Concept (PoC) and does not offer a comprehensive check.

## What lead to the creation of this tool

We found that 8.2% percent of the most downloaded npm packages are officially deprecated, but due to inconsistent practices in handling package dependencies, the real number is much larger, closer to 21.2%. 

Moreover, some package maintainers, when confronted with security flaws, deprecate their packages instead of reporting them, getting a CVE assigned or remediating the vulnerabilities. These gaps can leave developers unaware that they are using unmaintained, vulnerable packages, and create opportunities for attackers to take over unmaintained code that continues to be used.

![funnel (2)](https://github.com/Aqua-Nautilus/Dependency-Deprecated-Checker/assets/29836366/129ae729-6e53-40b6-b5d2-bca471617aec)

More information can be found on our [blog](https://blog.aquasec.com/deceptive-deprecation-the-truth-about-npm-deprecated-packages).

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
- `--github-token`: GitHub token for API access. This is mandatory unless `--exclude-archived` and `--exclude-inaccessible` are used.
- `--exclude-archived`: Exclude alerting on packages linked to archived repositories in GitHub.
- `--exclude-repo`: Exclude alerting on packages without an associated repository.
- `--exclude-inaccessible`: Exclude alerting on packages with a GitHub repository that is not accessible (404).


An example of the results on the sample package.json:


![final_example](https://github.com/Ilaygoldman/dependency_deprecated/assets/29836366/1e81e68d-7378-459e-aa40-89bc84300dd7)

