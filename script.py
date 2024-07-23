import csv
import os
import subprocess
import requests

project_dir = '.'
companies_dir = os.path.join(project_dir, 'Companies')
main_branch = 'main'
csv_file = os.path.join(project_dir, 'Remove_final.csv')

# Function to run shell commands
def run_command(command, cwd=project_dir):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

# Function to check if the branch exists
def branch_exists(branch_name):
    branches = run_command("git branch")
    return branch_name in branches

# Function to create a branch, commit, and push
def process_company(company_name):
    branch_name = f"remove-{company_name}"
    
    # Check if the branch already exists
    if branch_exists(branch_name):
        print(f"Branch {branch_name} already exists.")
        return
    
    # Create a new branch
    run_command(f"git checkout -b {branch_name}")
    
    # Delete the company directory
    company_dir = os.path.join(companies_dir, company_name)
    if os.path.isdir(company_dir):
        run_command(f"rm -rf {company_dir}")
    else:
        print(f"Directory {company_dir} does not exist")
        return
    
    # Check Git status before committing
    status_output = run_command("git status")
    print(f"Git status before commit:\n{status_output}")
    
    # Add changes
    run_command(f"git add {companies_dir}")
    
    # Commit the deletion
    commit_message = f"Removed Agent: {company_name} directory"
    commit_output = run_command(f"git commit -m '{commit_message}'")
    print(f"Commit output:\n{commit_output}")
    
    # Pull latest changes from the remote branch to avoid non-fast-forward errors
    pull_output = run_command(f"git pull --rebase origin {branch_name}")
    print(f"Pull output:\n{pull_output}")
    
    # Push the new branch
    push_output = run_command(f"git push origin {branch_name}")
    print(f"Push output:\n{push_output}")
    
    # Switch back to main branch and pull latest changes
    run_command(f"git checkout {main_branch}")
    run_command(f"git pull origin {main_branch}")

# Function to create PRs
def create_pr(branch_name, token, main_branch='main'):
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
    if response.status_code == 201:
        print(f"Pull request created for {branch_name}")
    else:
        print(f"Failed to create pull request for {branch_name}: {response.status_code} - {response.content.decode()}")


# Read the CSV file and process each company in batches
batch_size = 5  # Adjust batch size as needed
with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    companies = [row[0].strip() for row in csv_reader]

# Use your GitHub token from an environment variable
github_token = "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"  # Replace with your actual token

for i in range(0, len(companies), batch_size):
    batch = companies[i:i + batch_size]
    for company_name in batch:
        process_company(company_name)
        branch_name = f"remove-agent-{company_name}"
        create_pr(branch_name, github_token)
