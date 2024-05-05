import subprocess


def test_help():
    assert subprocess.call(['python', '-m', 'pycm', '--help']) == 0
