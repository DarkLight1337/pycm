import subprocess
import sys


def test_help():
    assert subprocess.call(['python', '-m', 'pycm', '--help']) == 0
    assert subprocess.call(['pycm', '--help'], shell=sys.platform == "win32") == 0
