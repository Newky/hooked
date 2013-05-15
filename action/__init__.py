#!/usr/bin/python2.7
import importlib
import json
import os


def get_config():
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    f = open(config_file, "r")
    contents = f.read()
    config = json.loads(contents)["hooks"]
    f.close()
    return config


def run(git_commit):
    config = get_config()
    for hook in config:
        hook_obj = importlib.import_module('%s.%s' % (__name__, hook))
        hook_func = getattr(hook_obj, "hook")
        hook_func(git_commit)
