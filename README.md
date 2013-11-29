Hooked
------

How to use
==========

Hooked is a python library for managing git hooks. It adds a plugin system to the git hooks which allow us to write simple python scripts to run for the different phases in git.

There are 3 different actions that can be done with hooked.py.

To demonstrate lets create a test git directory:

```
$ mkdir /tmp/testgit
$ cd /tmp/testgit
$ git init
```

None of the hooks are enabled in a normal git directory:

```
$ ls .git/hooks/
applypatch-msg.sample  pre-applypatch.sample      pre-rebase.sample
commit-msg.sample      pre-commit.sample      update.sample
post-update.sample     prepare-commit-msg.sample
```

In the hooked directory, we initialize the hooked system for that git repository.

```
$ python hooked.py --git-root=/tmp/testgit
```

Now, there is a few additions to the hooks directory:

```
$ ls .git/hooks/
action             post-update.sample     prepare-commit-msg
applypatch-msg.sample  pre-applypatch.sample  prepare-commit-msg.sample
commit-msg         pre-commit         pre-rebase.sample
commit-msg.sample      pre-commit.sample      update.sample
```

At time of writing, hooked.py creates prepare-commit-msg, commit-msg and pre-commit.
It also creates the action directory.

```
$ ls .git/hooks/action/
config.json  __init__.py  other_hook.py  test_hook.py
```

By default, it includes some example hooks but they are disabled. The config.json is a simple json configuration which lists which hooks are installed. By default, none are installed.

```
$ cat .git/hooks/action/config.json 
{ "hooks": [] }
```

Lets install some hooks, so hooks are stored outside the hooked repository as they are on a per user basis. lets create a git_hooks directory:

```
$ mkdir /tmp/git_hooks
$ cd /tmp/git_hooks
```

And lets make a python hook to demonstrate:

```
$ cat - > new_hook.py
def precommit(git_state):
    for fname in git_state["files"]:
        if "action" in fname:
            print "ARGGGGGHHHHHH"
            return False
    return True
```

This simply shouts if the word action is in the filename. Lets inject this into our git repo hooks. we can inject a directory or just a file. If you use a directory it will pull out all python files from the directory and all hooks that are copied will be turned on by default.

```
$ python hooked.py --git-root=/tmp/testgit --inject=/tmp/git_hooks/new_hook.py
```

Now lets look at the action folder and the contents of config.json:

```
$ ls .git/hooks/action/
config.json  __init__.py  new_hook.py  other_hook.py  test_hook.py
$ cat .git/hooks/action/config.json 
{"hooks": ["new_hook"]}
```

Your hooks have now been installed. If in the future you want to completely remove the usage of hooked.py you can do the following:

```
$ python hooked.py --git-root=/tmp/testgit --clean
```
