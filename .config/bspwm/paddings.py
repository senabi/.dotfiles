#!/usr/bin/python

import subprocess
from outputs import Outputs


def spawn_bspwm_cmd(monitor_paddings):
    for name, padding in monitor_paddings.items():
        subprocess.Popen(["bspc", "config", "-m",
                          name, "top_padding", padding],
                         close_fds=True)


def set_monitors(monitor_paddings={}):
    monitors = Outputs().get_list()
    if not monitor_paddings:
        for mon in monitors:
            monitor_paddings[mon["name"]] = "35"
        spawn_bspwm_cmd(monitor_paddings)
    else:
        if len(monitor_paddings) == len(monitors):
            print("equal")
            spawn_bspwm_cmd(monitor_paddings)
        else:
            print("not equal")
            for mon in monitors:
                if mon["name"] not in monitor_paddings:
                    monitor_paddings[mon["name"]] = "0"
            spawn_bspwm_cmd(monitor_paddings)


if __name__ == "__main__":
    set_monitors({})
