#!/usr/bin/python2.7
import os

from optparse import OptionParser

def fail(msg):
        print msg
        sys.exit(1)


def get_action_directory():
    return os.path.join(os.path.dirname(__file__), "action")


def copy_to_dotgit(options):
    if os.path.exist(options.gitroot):
        git_hook_path = os.path.join(
            options.gitroot, ".git/hooks")
        if os.path.exist(git_hook_path):
            shutil.copytree(get_action_directory(),
                    os.path.join(git_hook_path, "action")
        else:
            fail("directory is not a git repo or has no hooks"
                "directory")
    else:
        fail("git root does not exist")


if __name__ == "__main__":
    usage = "%prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--git-root", dest='gitroot',
            help=('the root directory of the git folder '
                'to inject hook'))
    (option, args) = parser.parse_args()
    copy_to_dotgit(options)
