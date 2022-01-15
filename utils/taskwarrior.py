import subprocess


def run_task(*args: str):
    return subprocess.run(['task', *args],
                          capture_output=True,
                          text=True)


def list_from_newline(output: str):
    if len(output) > 0:
        return output.strip('\n').split('\n')
    else:
        return []


def list_domains():
    domains = run_task('_projects')
    return list_from_newline(domains.stdout)
