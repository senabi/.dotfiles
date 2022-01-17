#!/usr/bin/env python

from Xlib import X, display
from Xlib.ext import randr
import os
import subprocess
import time

"""
https://color.firefox.com/?theme=XQAAAALlAQAAAAAAAABBqYhm849SCia-yK6EGccwS-xMDPr8MglS1IAYgPpJmMqoaMV1vHn7RqxNlu8tOtRSYRIcoLxg_ZR_1ASXilKo1LWlQaxU-HM8JLcbN29KiS6okgdHjvRfkVJOqjoBsScHEEQnbKiuLr9bKMyElvfnqzRnUr1bU1kLiHf9kRRVBj6kgPs_ghLvHwKTqZghKcm9AHnChaiPzl_4_DGGAXftkCG5RKsCCOYDkzBNCAFZxFrQmnGjGAMTaJxya0S-pmtZ3aB_HlQaYOj9V-IO1S1LS440PAwMGChw7cPMLF8tYrT9TiwRWqZ8d6CwW4sSuqUxm5H_ptbVoA
"""


def find_mode(id, modes):
    for mode in modes:
        if id == mode.id:
            return f"{mode.width}x{mode.height}"

def get_display_info():
    d = display.Display(':0')
    screen_count = d.screen_count()
    default_screen = d.get_default_screen()
    result = []
    screen = 0
    info = d.screen(screen)
    window = info.root

    res = randr.get_screen_resources(window)
    for output in res.outputs:
        params = d.xrandr_get_output_info(output, res.config_timestamp)
        if not params.crtc:
            continue
        crtc = d.xrandr_get_crtc_info(params.crtc, res.config_timestamp)
        modes = set()
        for mode in params.modes:
            modes.add(find_mode(mode, res.modes))
        result.append({
            'name': params.name,
            'resultion': f"{crtc.width}x{crtc.height}",
            'available_resolution': list(modes)
            })

    return result

display_info = get_display_info()
os.system("killall -q polybar")
time.sleep(2)

config = f"{os.environ['HOME']}/.config/polybar/config.ini"
polybar_proc = lambda name,env: subprocess.Popen(["polybar", name, "-c", config], env=env, close_fds=True)

match len(display_info):
    case 1:
        os.environ['MONITOR'] = display_info[0]['name']
        env = os.environ.copy()
        procs = ["workspace", "keyboard", "time", "audio", "stats_single_mon", "tray_single_mon", "background"]
        for name in procs[:-1]:
            polybar_proc(name,env)
        time.sleep(2)
        polybar_proc(procs[-1],env)
    case 2:
        os.environ['MONITOR'] = display_info[0]['name']
        env = os.envirion.copy()
        first_procs = ["workspace", "keyboard", "time", "audio"]
        sec_procs = ["workspace@v2", "stats", "tray", "background"]
        for name in first_procs:
            polybar_proc(name, env)
        env['MONITOR'] = display_info[1]['name']
        for name in sec_procs[:-1]:
            polybar_proc(name,env)
        time.sleep(2)
        polybar_proc(sec_procs[-1], env)

