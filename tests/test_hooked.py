import os
import shutil
import unittest

from subprocess import check_call, CalledProcessError, PIPE


class TestHookedIsFunctional(unittest.TestCase):
    def setUp(self):
        super(TestHookedIsFunctional, self).setUp()
        self.old_dir = os.getcwd()
        os.mkdir("test_directory")
        os.chdir("test_directory")
        check_call(["git", "init"])
        os.chdir(self.old_dir)
        # hooked binary
        self.hooked_binary = "./hooked.py"
        self.git_root_dir = os.path.join(os.getcwd(), "test_directory")

    def tearDown(self):
        shutil.rmtree(self.git_root_dir)
        os.chdir(self.old_dir)
        super(TestHookedIsFunctional, self).tearDown()

    def test_hooked_installs_hooks_success(self):
        # dirty hack, I have no internets
        os.chdir("..")
        git_hooks_path = os.path.join(self.git_root_dir, ".git/hooks/")
        current_hooks = os.listdir(git_hooks_path)
        out = check_call([self.hooked_binary, "--git-root=%s" % (self.git_root_dir)])
        hooked_hooks = os.listdir(git_hooks_path)
        different_hooks = set(hooked_hooks) - set(current_hooks)
        self.assertEquals(different_hooks, set(["action", "prepare-commit-msg", "pre-commit"]))

    def test_hooked_no_git_root(self):
        # dirty hack, I have no internets
        # install hooks
        os.chdir("..")
        try:
            out = check_call([self.hooked_binary])
            self.assertEquals(out, 0, "This should not execute")
        except CalledProcessError:
            # test worked!
            pass


if __name__ == "__main__":
    unittest.main()
