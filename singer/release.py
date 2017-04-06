import distutils
import subprocess

def git(*args):
    cmd = ['git'] + list(args)

    print('> {}'.format(' '.join(cmd)))
    lines = str(subprocess.check_output(cmd, universal_newlines=True)).splitlines()
    for line in lines:
        print(line)
    print('')
    return lines


def fail(msg):
    print(msg)
    exit(1)


def git_check_branch():
    branch_lines = git('rev-parse', '--abbrev-ref', 'HEAD')
    if len(branch_lines) == 0:
        fail('Could not determine branch')
    branch = branch_lines[0]
    if branch != 'master':
        fail('Must be on master branch, you are on {}'.format(branch))

def git_check_status():
    status_lines = git('status', '--porcelain')
    if len(status_lines) > 0:
        fail('You have uncommitted changes')

def git_push():
    git('push')

class Release(distutils.cmd.Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        git_check_branch()
        git_check_status()
        git_push()

        # @# there must also be no files in the git index. We will make a commit after
        # @# the apply and we only want to commit production.tfstate
        # [ -z "$$(git status --porcelain)" ]

