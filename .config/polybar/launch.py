#!env python

from Xlib import display
import sys
import time
import os
import subprocess

"""
https://color.firefox.com/?theme=XQAAAALlAQAAAAAAAABBqYhm849SCia-yK6EGccwS-xMDPr8MglS1IAYgPpJmMqoaMV1vHn7RqxNlu8tOtRSYRIcoLxg_ZR_1ASXilKo1LWlQaxU-HM8JLcbN29KiS6okgdHjvRfkVJOqjoBsScHEEQnbKiuLr9bKMyElvfnqzRnUr1bU1kLiHf9kRRVBj6kgPs_ghLvHwKTqZghKcm9AHnChaiPzl_4_DGGAXftkCG5RKsCCOYDkzBNCAFZxFrQmnGjGAMTaJxya0S-pmtZ3aB_HlQaYOj9V-IO1S1LS440PAwMGChw7cPMLF8tYrT9TiwRWqZ8d6CwW4sSuqUxm5H_ptbVoA
"""


class Outputs:
    def __init__(self):
        self.d = display.Display()
        if not self.d.has_extension('RANDR'):
            sys.stderr.write(
                f'{sys.argv[0]}: server does not have the RANDR extension\n')
            ext = self.d.query_extension('RANDR')
            print(ext)
            sys.stderr.write("\n".join(self.d.list_extensions()))
            if ext is None:
                sys.exit(1)

        # current screen
        self.screen = self.d.screen()
        resources = self.screen.root.xrandr_get_screen_resources()._data

        self.outputs_list = []
        for output in resources['outputs']:
            output_info = self.d.xrandr_get_output_info(
                output, resources['config_timestamp'])._data
            if not output_info['crtc']:
                continue
            # self.pp.pprint(output_info)
            crtc = self.d.xrandr_get_crtc_info(
                output_info['crtc'], resources['config_timestamp'])._data
            self.outputs_list.append(
                {'name': output_info['name'],
                    'height': crtc['height'], 'width': crtc['width']})

    def get_list(self):
        return self.outputs_list


config = f"{os.environ['HOME']}/.config/polybar/config.ini"


def module_proc(name, env):
    return subprocess.Popen(["polybar", name, "-c", config],
                            env=env, close_fds=True)


def set_monitor(env={}, name=None):
    env["MONITOR"] = name
    return env


def exec_modules(modules_per_mon, outputs):
    # len(modules) == len(outputs)
    # execute background modules
    env = os.environ.copy()
    for mon_idx, modules in enumerate(modules_per_mon):
        if modules is None:
            continue
        mon_name = outputs[mon_idx]["name"]
        env = set_monitor(env, mon_name)
        for module in modules:
            module_proc(module, env)
            print(module, env)
    time.sleep(2)
    for output in outputs:
        env = set_monitor(env, output["name"])
        module_proc("background", env)


if __name__ == "__main__":
    outputs = Outputs().get_list()
    os.system("killall -q polybar")
    time.sleep(2)
    modules = [None]*len(outputs)
    if len(outputs) == 1:
        modules[0] = [
            "workspace@mon1",
            "keyboard@mon1",
            "time@mon1",
            "audio@mon1",
            "stats@mon1",
            "tray@mon1",
        ]

    elif len(outputs) > 1:
        # first monitor
        modules[0] = ["workspace@mon1",
                      "keyboard@mon1", "time@mon1", "audio@mon1"]
        # second monitor
        modules[1] = ["workspace@mon2", "stats@mon2", "tray@mon2"]

    exec_modules(modules, outputs)
