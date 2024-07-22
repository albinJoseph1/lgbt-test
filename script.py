import csv
import os
import subprocess

# Define paths and main branch name
project_dir = '/home/yatnam/projects/lgbtjobs/script/lgbt-test'
companies_dir = os.path.join(project_dir, 'Companies')
main_branch = 'main'
csv_file = os.path.join(project_dir, 'remove.csv')

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

# Function to create a branch, commit, and push
def process_company(company_name):
    branch_name = f"remove-agent-{company_name}"
    
    # Delete the company directory
    company_dir = os.path.join(companies_dir, company_name)
    if os.path.isdir(company_dir):
        run_command(f"rm -rf {company_dir}")
    else:
        print(f"Directory {company_dir} does not exist")
        return
    
    # Create a new branch
    run_command(f"git checkout -b {branch_name}")
    
    # Commit the deletion
    run_command(f"git add {companies_dir}")
    run_command(f"git commit -m 'Remove {company_name} directory'")
    
    # Push the new branch
    run_command(f"git push origin {branch_name}")
    
    # Switch back to main branch and pull latest changes
    run_command(f"git checkout {main_branch}")
    run_command(f"git pull origin {main_branch}")

# Read the CSV file and process each company
with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        company_name = row[0].strip()
        process_company(company_name)

# Function to create PRs (this will need your GitHub token)
import requests

# Function to create PRs (this will need your GitHub token)
def create_pr(branch_name, token):
    url = f"https://api.github.com/repos/albinJoseph1/lgbt-test/pulls"
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
        print(f"Failed to create pull request for {branch_name}: {response.content}")

# Use your GitHub token
github_token = "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"

# Read the CSV file again to create PRs
with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        company_name = row[0].strip()
        branch_name = f"remove-agent-{company_name}"
        create_pr(branch_name, github_token)
