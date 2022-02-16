#!/usr/bin/python

from outputs import Outputs
import subprocess


def spawn_workspaces(monitor, length):
    args = ["bspc", "monitor", monitor, "-d"]
    args += [str(w) for w in range(length)]
    subprocess.Popen(args, close_fds=True)


if __name__ == '__main__':
    monitors = Outputs().get_list()
    if len(monitors) == 0:
        exit(1)
    spawn_workspaces(monitors[0]["name"], 5)
    if len(monitors) >= 2:
        spawn_workspaces(monitors[1]["name"], 3)
