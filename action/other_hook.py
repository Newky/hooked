import time

def precommit(git_state):
    for fname in git_state["files"]:
        if "action" in fname:
            print "ARGGGGGHHHHHH"
            return False
    return True
