#!/usr/bin/python2.7
import os
import shutil
import stat

from optparse import OptionParser


GIT_HOOKS = ["pre-commit.py"]

def fail(msg):
        print msg
        sys.exit(1)


def get_action_directory():
    return os.path.join(os.path.dirname(__file__), "action")


def clean_up_dotgit(options):
    git_hook_path = get_git_path(options)
    for hook in GIT_HOOKS:
        git_hook_name = git_hook_rename(hook)
        os.remove(os.path.join(git_hook_path, git_hook_name))
    shutil.rmtree(os.path.join(git_hook_path, "action"))


def git_hook_rename(hook):
    return hook.replace(".py", "")


def make_executable(file_path):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)


def copy_git_hooks_to_dotgit(options):
    git_hook_path = get_git_path(options)
    for hook in GIT_HOOKS:
        git_hook_name = git_hook_rename(hook)
        git_hook_full_path = os.path.join(git_hook_path, git_hook_name)
        shutil.copy(hook, git_hook_full_path)
        make_executable(git_hook_full_path)


def copy_action_dir_to_dotgit(options):
    git_hook_path = get_git_path(options)
    shutil.copytree(get_action_directory(),
            os.path.join(git_hook_path, "action"))


def get_git_path(options):
    if os.path.exists(options.gitroot):
        git_hook_path = os.path.join(
            options.gitroot, ".git/hooks")
        if os.path.exists(git_hook_path):
            return git_hook_path
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
    parser.add_option("--clean", dest='clean', action='store_true',
            default=False, help=('Clean up after yourself'))
    (options, args) = parser.parse_args()
    if options.clean:
        clean_up_dotgit(options)
    else:
        copy_action_dir_to_dotgit(options)
        copy_git_hooks_to_dotgit(options)
