import argparse
import json
import traceback
import requests
import github_api_request_handler as gh
import concurrent.futures

dict_of_deprecated = {}

def parse_package_json_file(config):
	file_path =config.package_json_file
	package_dependencies = []

	with open(file_path) as f:
		package_json_content = json.loads(f.read())

	if 'dependencies' in package_json_content:
		package_dependencies = list(package_json_content['dependencies'].keys())

	return package_dependencies


def scan_packages(packages, config):
	unique_package_list = set(packages)

	# scan all packages using threads
	with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		for package in unique_package_list:
			executor.submit(scan_package_for_dependency_deprecated, package, config)


def extract_github_repo_from_package_info(package_info):
    # no repository information
    if 'repository' not in package_info or package_info['repository'] is None:
        return ""

    # now we need to check format of how the repository information is shown
    if type(package_info['repository']) is str:
        github_repo = package_info['repository'].lower()
    elif type(package_info['repository']) is dict:
        if 'url' not in package_info['repository'] or package_info['repository']['url'] is None:
            return ""
        github_repo = package_info['repository']['url'].lower()
    else:
    	# unknown format should not reach here
    	return ""
    
    # This is incase the repository is not in github
    if 'github.com' not in github_repo:
        return ""

    # now we convert all the types of github repos to that same format
    if github_repo.startswith('git+'):
        github_repo=github_repo[4:]
    if github_repo.startswith('ssh://'):
        github_repo=github_repo[len('ssh://'):]
    if github_repo.startswith('git://'):
        github_repo=github_repo.replace('git://', 'https://')
    if github_repo.startswith('git@github.com:'):
        github_repo=github_repo.replace('git@github.com:', 'https://github.com/')
    if github_repo.startswith('git@github.com'): # this is in case there is no : in it
        github_repo=github_repo.replace('git@github.com', 'https://github.com')
    if github_repo.endswith('.git'):
        github_repo=github_repo[:-len('.git')]

    # clean all trailing /
    while github_repo.endswith('/'):
        github_repo=github_repo[:-1]
    return github_repo


# this function assumes there is no leading '/' at the end
def get_repo_from_github_url(github_repo_link):
    repo_parts_list = github_repo_link.split("/")
    if len(repo_parts_list) >= 5:
        return (repo_parts_list[3],repo_parts_list[4])

    # this means we dont have a good format of the github_link so we cant scan it
    return (None, None)

def check_github_archived(org ,repo, config):
    url = f"https://api.github.com/repos/{org}/{repo}"
    resp = gh.get(url, config.github_token)

	# if its 404 we currently do not declare archived because maybe it became private etc'
    if resp.status_code != 200:
        return False
    results = resp.json()

    return results['archived']

def is_function_directly_deprecated(package_name, npm_response_json, config):
	# check if this package is deprecated
	if 'deprecated' in npm_response_json:
		return True

	# check if the user disabled the no_repo check
	if not config.exclude_repo:
		if 'repository' not in npm_response_json:
			return True

	# check if the user disabled the github archived check
	if not config.exclude_archived:
		github_repo = extract_github_repo_from_package_info(npm_response_json)

		# if we couldnt extract the GitHub repository for various reasons (repo wasn't GitHub for example)
		if github_repo == "":
			return False

		org, repo = get_repo_from_github_url(github_repo)

		# if we couldnt extract the org/repo info from the github_link
		if org == None:
			return False

		if check_github_archived(org, repo, config):
			return True

	return False

	# now we check only if the flags 

def scan_package_for_dependency_deprecated(package_name, config, list_of_parrent=[]):
	try:

		# here we check if we already scanned this package
		if package_name in dict_of_deprecated:
			return dict_of_deprecated[package_name]
	
		url=f'https://registry.npmjs.com/{package_name}/latest'
		
		resp = requests.get(url)
		if resp.status_code != 200:
			print(f'error in {package_name}')
			dict_of_deprecated[package_name]="" # default value is not deprecated
			return ""
	
		resp_json = resp.json()

		# here we check if the package is directly deprecated. also depends on the flags from the user (check github, etc')
		if is_function_directly_deprecated(package_name, resp_json, config):
			dict_of_deprecated[package_name] = package_name
			return package_name
	
		if 'dependencies' not in resp_json:
		#	with locki:
			dict_of_deprecated[package_name] = ""
			return ""
	
		dict_of_dependencies = resp_json['dependencies']
		list_of_depndencies = dict_of_dependencies.keys()
	
		# now we check if one of the dependencies was already found deprecated. this is so we wont go by a different order and check other dependencies when we already have one
		for dependency_package in list_of_depndencies:
			if dependency_package in dict_of_deprecated and dict_of_deprecated[dependency_package] != "":
				#with locki:
				dict_of_deprecated[package_name] = dependency_package

				return dependency_package
	
		# here we do not consider the versions
		for dependency_package in dict_of_dependencies.keys():

			# preventing infinite loops
			if dependency_package in list_of_parrent:
				continue
	
			dependent_package_name_deprecated = scan_package_for_dependency_deprecated(dependency_package, config, list_of_parrent + [package_name])
	
			# if the dependent package is dependent on a deprecated package
			if dependent_package_name_deprecated != "":
				#with locki:
				#dict_of_deprecated[package_name] = dependent_package_name_deprecated
				dict_of_deprecated[package_name] = dependency_package

				#return dependent_package_name_deprecated
				return dependency_package

		dict_of_deprecated[package_name] = ""
	except Exception as e:
		print(e)
		traceback.print_exc()

		# if there is an exception in the scan we will mark it as not deprecated for the moment
		if package_name not in dict_of_deprecated:
			dict_of_deprecated[package_name] = ""

	return ""


def main():
	parser = argparse.ArgumentParser(description="scan package.json for dependencies that are deprecated directly and indirectly")

	parser.add_argument("package_json_file", nargs="?", default='package.json', help="path to pacakge.json file, default is 'package.json'")

	parser.add_argument("--github-token", nargs="?", help="GitHub token to use for the api, no permissions needed. This is mandatory unless you state the --exclude-archived flag")

	# do not include github archived repositories in the scan
	parser.add_argument("--exclude-archived", action='store_true', help="Do not alert on packages whose GitHub repositories are archived. Defaults to False")

	# do not alert on packages that do not point to a repository
	parser.add_argument("--exclude-repo", action='store_true', help="Do not alert on packages that are not associated with a repository. Defaults to False.")


	# Parse the command-line arguments
	args = parser.parse_args()

	if not args.exclude_archived and not args.github_token:
		parser.error('You must provide a readonly GitHub token. If you do not want to scan for archived repositories you can use the --exclude-archived flag')


	list_of_depndency_packages = parse_package_json_file(args)

	scan_packages(list_of_depndency_packages, args)

	print('checking if dependencies are deprecated:')
	for package in list_of_depndency_packages: 
		if dict_of_deprecated[package]!="":
			# now we print the chain of deprecation
			chain_of_dep_str=package
			current_package=package

			# we stop only when we get to the package which is directly deprecated
			while  dict_of_deprecated[current_package]!=current_package:
				chain_of_dep_str += " -> " + dict_of_deprecated[current_package]
				current_package = dict_of_deprecated[current_package]
			print(f'package {package} is deprecated, chain of dependency is [{chain_of_dep_str}]')


if __name__ == '__main__':
	main()