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
source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh

#aliases
[ -f "$HOME/.config/zsh/aliases.sh" ] && source "$HOME/.config/zsh/aliases.sh"

# source "$NVM_DIR/nvm.sh"
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk

if [[ ${XDG_SESSION_TYPE} = "x11" ]]; then
  eval "$(starship init zsh)"
  # >>> conda initialize >>>
  # !! Contents within this block are managed by 'conda init' !!
  __conda_setup="$('/home/baddra/.local/share/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
  if [ $? -eq 0 ]; then
      eval "$__conda_setup"
  else
      if [ -f "/home/baddra/.local/share/anaconda3/etc/profile.d/conda.sh" ]; then
# . "/home/baddra/.local/share/anaconda3/etc/profile.d/conda.sh"  # commented out by conda initialize
      else
# export PATH="/home/baddra/.local/share/anaconda3/bin:$PATH"  # commented out by conda initialize
      fi
  fi
  unset __conda_setup
  # <<< conda initialize <<<

  # nvm nodejs
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"  # This loads nvm
  [ -s "$NVM_DIR/bash_completion" ] && source "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
fi

