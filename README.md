Hooked
------

Introduction
============

This python module allows for a nice git hook flow.

It is designed with a run time similar to django middleware. Git hooks should just be a normal python class which exposes a function with the following declaration:

    Class HookPlugin():
        def hook(git_commit):
            # hook logic

git\_commit is a state like object which is defined in this project and exposes things like modified files and other useful information to each hook. git\_commit is mutatable so this should be considered when combining the hooks.
