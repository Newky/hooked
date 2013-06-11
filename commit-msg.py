#!/usr/bin/python2.7
import sys

from action import run

PHASE = "commitmsg"
commit_file_path = sys.argv[1]

git_state = {"commit_file_path": commit_file_path}

hook_results = run(PHASE, git_state)

is_commitable = all(hook_results)

if not is_commitable:
    sys.exit(1)
