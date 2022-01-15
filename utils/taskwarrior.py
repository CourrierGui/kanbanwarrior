import subprocess

def run_task(*args: str):
    return subprocess.run(['task', *args],
                          capture_output=True,
                          text=True)

def list_domains():
    domains = run_task('_projects')
    if len(domains.stdout) > 0:
        return domains.stdout.split('\n')
    else:
        return []
