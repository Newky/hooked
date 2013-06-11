def precommit(git_state):
    print git_state["files"]
    return True


def preparecommitmsg(git_state):
    print "COMMIT MSG is %s" % git_state["commit_file_path"]

    return True

def commitmsg(git_state):
    print "After the fact"
    with open(git_state["commit_file_path"], "r") as commit:
        print commit.read()

    return True
