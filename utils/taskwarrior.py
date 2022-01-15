import subprocess
import json


default_tags = {
  'ACTIVE', 'ANNOTATED',
  'BLOCKED', 'BLOCKING',
  'CHILD', 'COMPLETED',
  'DELETED', 'DUE',
  'DUETODAY', 'INSTANCE',
  'LATEST', 'MONTH',
  'ORPHAN', 'OVERDUE',
  'PARENT', 'PENDING',
  'PRIORITY', 'PROJECT',
  'QUARTER', 'READY',
  'SCHEDULED', 'TAGGED',
  'TEMPLATE', 'TODAY',
  'TOMORROW', 'UDA',
  'UNBLOCKED', 'UNTIL',
  'WAITING', 'WEEK',
  'YEAR', 'YESTERDAY',
  'next', 'nocal',
  'nocolor', 'nonag',
}

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


def list_projects():
    projects = run_task('_tags')
    tags = list_from_newline(projects.stdout)
    return list(set(tags).difference(default_tags))


def list_pending(*args: str):
    return json.loads(run_task('status:pending', *args, 'export').stdout)
