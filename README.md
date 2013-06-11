Hooked
------

Introduction
============

This python module allows for a nice pluginable system for git hooks. It is meant to be easily extendable.

An article on how to write a new git hook:
<a href="http://richydelaney.com/snippets/hooked---my-new-python-package-for-managing-git-hooks.html">Manage your git hooks</a>

First lets familiarize ourselves with the relevant files:

__hooked/hooked.py:__


- This is the command line script to inject the git hook files and relevant other files for running git hooks.
- It also contains a --clean which will clean up damage done. (well, kind of).

__hooked/pre-commit.py:__


- This is the first example I have added, this gets copied to the .git/hooks/pre-commit. It basically calls action.run() and passes the relevant phase into this function.
- It is responsible for passing in a "git\_state", what does this mean? In this case it is the files that will be in this commit, but can be differing things depending on what is relevant at this stage of the commit process.


__hooked/action/\_\_init\_\_.py:__


- This is where the (bad) magic happens. This exposes a function called run() which takes a phase (just a string, for example "precommit", and takes a relevant git state)

- It then imports all other files in the action directory and grabs any functions named the same as phase variable passed in. Executes these functions using the git state thats passed in.
- It collects and returns a list of all the return values of the git hooks.

An example pre-commit hook is listed here:

__action/test\_hook.py__


Conclusion
==========

In order to write a git hook now, all that you have to do is write a new (or existing file which doesn't have it defined) python file with a function named after the phase you want (i.e def precommit(git\_state))

This will be picked up by action.run() and will be run on every commit at that phase. Before you write your git hook, make sure that the relevant phase has a corresponding action file in the root directory, for example at time of writing the following have been defined:

- pre-commit.py
- prepare-commit-msg.py

If the phase you want is there, it should be trivial to implement a different one and pass in the state you want. Pull requests are welcome.
