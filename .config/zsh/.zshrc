HISTSIZE=2000
SAVEHIST=2000
HISTFILE=$HOME/.cache/zsh/history

autoload -U compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' rehash true
zmodload zsh/complist
_comp_options+=(globdots)
typeset -a ealiases
ealiases=()

function abbr() {
    alias $1
    ealiases+=(${1%%\=*})
}

function expand-ealias(){
    if [[ $LBUFFER =~ "\<(${(j:|:)ealiases})\$" ]]; then
        zle _expand_alias
	zle _expand_word
    fi
    zle magic-space
}
zle -N expand-ealias
unsetopt BEEP

bindkey ' ' expand-ealias
bindkey '^ ' magic-space
bindkey -M isearch " " magic-space

expand-alias-and-accept-line() {
    expand-ealias
    zle .backward-delete-char
    zle .accept-line
}
zle -N accept-line expand-alias-and-accept-line

autoload edit-command-line; zle -N edit-command-line
bindkey '^e' edit-command-line
bindkey -M menuselect 'h' vi-backward-char
bindkey -M menuselect 'k' vi-up-line-or-history
bindkey -M menuselect 'l' vi-forward-char
bindkey -M menuselect 'j' vi-down-line-or-history
bindkey -v '^?' backward-delete-char
bindkey -s ^f "tmux-sessionizer\n"
bindkey -s ^t "tmux\n"

#plugins
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

#aliases
[ -f "$HOME/.config/zsh/aliases.sh" ] && source "$HOME/.config/zsh/aliases.sh"

#prompt
eval "$(starship init zsh)"
