import csv
import os
import subprocess
import requests

# Define paths and main branch name
project_dir = '/home/yatnam/projects/lgbtjobs/script/lgbt-test'
companies_dir = os.path.join(project_dir, 'Companies')
main_branch = 'main'
csv_file = os.path.join(project_dir, 'remove.csv')

# Function to run shell commands
def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

# Function to create a branch, commit, and push
def process_company(company_name):
    branch_name = f"remove-agent-{company_name}"
    
    # Delete the company directory
    company_dir = os.path.join(companies_dir, company_name)
    if os.path.isdir(company_dir):
        run_command(f"rm -rf {company_dir}", cwd=project_dir)
    else:
        print(f"Directory {company_dir} does not exist")
        return
    
    # Create a new branch
    run_command(f"git checkout -b {branch_name}", cwd=project_dir)
    
    # Commit the deletion
    run_command(f"git add {companies_dir}", cwd=project_dir)
    run_command(f"git commit -m 'Remove {company_name} directory'", cwd=project_dir)
    
    # Push the new branch
    run_command(f"git push origin {branch_name}", cwd=project_dir)
    
    # Switch back to main branch and pull latest changes
    run_command(f"git checkout {main_branch}", cwd=project_dir)
    run_command(f"git pull origin {main_branch}", cwd=project_dir)

# Function to check if branch exists
def check_branch_exists(branch_name, token):
    url = f"https://api.github.com/repos/albinJoseph1/lgbt-test/branches/{branch_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200

# Function to create PRs
def create_pr(branch_name, token):
    if not check_branch_exists(branch_name, token):
        print(f"Branch {branch_name} does not exist.")
        return
    
    url = "https://api.github.com/repos/albinJoseph1/lgbt-test/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": f"PR for {branch_name}",
        "head": branch_name,
        "base": main_branch
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Creating PR with data: {data}")
    print(f"API URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode()}")
    if response.status_code == 201:
        print(f"Pull request created for {branch_name}")
    else:
        print(f"Failed to create pull request for {branch_name}: {response.status_code} - {response.content.decode()}")

# Use GitHub token from environment variable
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("GitHub token not found. Set the GITHUB_TOKEN environment variable.")
else:
    # Read the CSV file and process each company
    if os.path.getsize(csv_file) == 0:
        print("CSV file is empty.")
    else:
        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                company_name = row[0].strip()
                process_company(company_name)
                
                branch_name = f"remove-agent-{company_name}"
                create_pr(branch_name, github_token)
