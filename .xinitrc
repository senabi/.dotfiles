#!/usr/bin/bash

export _JAVA_AWT_WM_NONREPARENTING=1
export EDITOR=nvim
export VISUAL=nvim
export TERMINAL=kitty
export ZDOTDIR=$HOME/.config/zsh
export PATH=$HOME/.local/bin:$PATH
export PATH=$HOME/go/bin:$PATH
export XDG_CONFIG_HOME=$HOME/.config
export XDG_CACHE_HOME=$HOME/.cache
export XDG_DATA_HOME=$HOME/.local/share
export BROWSER=firefox
export CC=clang
export CXX=clang++
export QT_STYLE_OVERRIDE=kvantum
export DENO_INSTALL=/home/toa/.deno
export PATH=$DENO_INSTALL/bin:$PATH
export XDG_SESSION_TYPE=x11
export GDK_BACKEND=x11

# vm
# xrandr -s 1600x900

#input
setxkbmap -layout us,es -option grp:alt_shift_toggle
setxkbmap -option caps:escape
xset r rate 300 50
xset m 0 0
xinput --set-prop 9 'libinput Accel Profile Enabled' 0, 1
xinput --set-prop 10 'libinput Accel Speed' -1
xsetroot -cursor_name left_ptr

# /usr/libexec/polkit-gnome-authentication-agent-1 &
# dunst &
picom --animations --animation-window-mass 0.5 --animation-for-open-window zoom --animation-stiffness 350 &
nitrogen --restore &
nm-applet &
# pasystray &

#paths
source ${HOME}/.cargo/env
# exec dbus-run-session bspwm
# exec bspwm
exec dbus-launch bspwm
