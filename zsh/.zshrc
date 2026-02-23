# Start profiling .zshrc (for performance issue)
# zmodload zsh/zprof

# Disable ohmyzsh autoupdate
ZSH_DISABLE_AUTO_UPDATE=true
ZSH_DISABLE_COMPFIX=true

# Smarter completion initialization
autoload -Uz compinit
if [ "$(date +'%j')" != "$(stat -f '%Sm' -t '%j' ~/.zcompdump 2>/dev/null)" ]; then
    compinit
else
    compinit -C
fi

# If you come from bash you might have to change your $PATH.
export PATH=/opt/nvim-linux-x86_64/bin:$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time Oh My Zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="spaceship"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git spaceship-vi-mode fzf)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"
export EDITOR="nvim"
export SUDO_EDITOR="/opt/nvim-linux-x86_64/bin/nvim"

# You may need to manually set your language environment
export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# History settings
# Set the ":start:elapsed;command" format
setopt EXTENDED_HISTORY
# Share history between sessions
setopt SHARE_HISTORY
# Write to the history file immediately
setopt INC_APPEND_HISTORY
# Don't write entries starting with a space
setopt HIST_IGNORE_SPACE
# Do not display a line previously found
setopt HIST_FIND_NO_DUPS
# Don't write duplicate entries
setopt HIST_SAVE_NO_DUPS
# Don't record an entry that was just recorded again
setopt HIST_IGNORE_DUPS
# Delete old entry if new entry is a duplicate
setopt HIST_IGNORE_ALL_DUPS
# Expire duplicate entries first when trimming
setopt HIST_EXPIRE_DUPS_FIRST
# Remove superfluous blanks before recording
setopt HIST_REDUCE_BLANKS

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

alias bat="batcat"
alias sudo="sudo --preserve-env"
alias tree="tree -C"
alias vimdiff="nvim -d"
alias vim="nvim"

# Enable vi mode
bindkey -v
eval spaceship_vi_mode_enable

# fzf: fuzzy file search
bindkey -r "^t"
bindkey "^f" fzf-file-widget
# ctrl + k: delete the line
bindkey "^k" kill-whole-line
# ctrl + e: goto end of line
bindkey "^e" end-of-line
# ctrl + a: goto beginning of line
bindkey "^a" beginning-of-line

# Setup zoxide
eval "$(zoxide init zsh --cmd cd)"

# Shitty script for zsh to autocomplete my 10 billion servers ...
source ~/.config/ssh_completion.zsh

# Stop profiling .zshrc (for performance issue)
# zprof
