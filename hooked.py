#!/usr/bin/python2.7
import json
import os
import shutil
import stat
import sys

from optparse import OptionParser


GIT_HOOKS = ["pre-commit.py", "prepare-commit-msg.py", "commit-msg.py"]


def fail(msg):
    print msg
    sys.exit(1)


def get_action_directory():
    return os.path.join(os.path.dirname(__file__), "action")


def clean_up_dotgit(options):
    git_hook_path = get_git_path(options)
    for hook in GIT_HOOKS:
        git_hook_name = git_hook_rename(hook)
        hook_path = os.path.join(git_hook_path, git_hook_name)
        if os.path.exists(hook_path):
            os.remove(hook_path)
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
        if os.path.exists(git_hook_full_path):
            backup_path = git_hook_full_path + ".bak"
            shutil.copy(git_hook_full_path, backup_path)
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


def find_file_root(full_filename):
    filename = os.path.basename(full_filename)
    return filename[:filename.rfind(".py")]


def inject_file(options):
    if not os.path.exists(options.injectlocation):
        fail("location to inject does not exist")

    if os.path.isfile(options.injectlocation):
        files = [options.injectlocation]
    elif os.path.isdir(options.injectlocation):
        for dirname, _, files in os.walk(options.injectlocation):
            if dirname == options.injectlocation:
                break
        files = [os.path.join(options.injectlocation, f)
                for f in files
                if f.endswith(".py")]

    git_hook_path = get_git_path(options)
    action_path = os.path.join(git_hook_path, "action/")
    action_config_filename = os.path.join(action_path, "config.json")
    config = {}

    for fname in files:
        shutil.copy(fname, action_path)

    with open(action_config_filename, "r") as action_config_file:
        config = json.load(action_config_file)

    for fname in files:
        hook_name = find_file_root(fname)
        if hook_name not in config["hooks"]:
            config["hooks"].append(hook_name)

    with open(action_config_filename, "w") as action_config_file:
        json.dump(config, action_config_file)


def check_command_line_arguments(options):
    mandatory = ["gitroot"]
    for field in mandatory:
        if not getattr(options, field, False):
            raise Exception("%s is a mandatory argument" % field)


def get_command_line_arguments():
    usage = "%prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--inject", dest='injectlocation',
            help=('takes the filename to inject and add to the config'))
    parser.add_option("--git-root", dest='gitroot',
            help=('the root directory of the git folder '
                'to inject hook'))
    parser.add_option("--clean", dest='clean', action='store_true',
            default=False, help=('Clean up after yourself'))
    (options, _) = parser.parse_args()
    return options


if __name__ == "__main__":
    options = get_command_line_arguments()
    check_command_line_arguments(options)
    if options.clean:
        clean_up_dotgit(options)
    elif options.injectlocation:
        inject_file(options)
    else:
        copy_action_dir_to_dotgit(options)
        copy_git_hooks_to_dotgit(options)
