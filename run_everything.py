import subprocess

# Replace 'script_to_run.py' with the actual name of the script you want to run
# script_path = 'scraping_and_sentiment.py'
script_path = '/Users/kmaurinjones/Desktop/ds/github_repos/DailyNewsDriftCanada/scraping_and_sentiment.py'
completed_process = subprocess.run(['python', script_path], capture_output=True, text=True)

print("Return Code:", completed_process.returncode)
print("Standard Output:", completed_process.stdout)
print("Standard Error:", completed_process.stderr)

def run_shell_script():
    # command = ['./git_auto_push.sh', 'Data updated and pushed to Github']
    command = ['/Users/kmaurinjones/Desktop/ds/github_repos/DailyNewsDriftCanada/git_auto_push.sh', 'data updated']
    result = subprocess.run(command)

    if result.returncode == 0:
        print('Command executed successfully!')
    else:
        print('Command failed.')

if __name__ == "__main__":
    run_shell_script()