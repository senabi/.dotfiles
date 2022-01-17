#!/usr/bin/bash

wid="${1}"
win_name="$(xprop -id ${wid} | grep -oP '_NET_WM_NAME\(UTF8_STRING\) = "\K[^"]*')"

[[ $win_name == "Library" ]] && echo "state=floating"
[[ $win_name == "Sign in"* ]] && echo "state=floating"
