def precommit(git_state):
    print git_state["files"]
    return True


def preparecommitmsg(git_state):
    with open(git_state["commit_file_path"], "r") as commit:
        print commit.read()

    return True
