#!/usr/bin/python2.7
import sys
from subprocess import check_output

from action import run

PHASE = "precommit"


def get_staged_files():
    command = ["git" ,"diff" ,"--cached" ,"--name-only"]
    output = check_output(command)
    # need to split it up
    files = output.split("\n")
    return [ f for f in files if f ]


git_state = {"files": get_staged_files()}

hook_results = run(PHASE, git_state)

is_commitable = all(hook_results)

if not is_commitable:
    sys.exit(1)
