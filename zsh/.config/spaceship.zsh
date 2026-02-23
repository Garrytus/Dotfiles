# Display username always
SPACESHIP_USER_SHOW=needed
# Render prompt asynchronously or not
SPACESHIP_PROMPT_ASYNC=true
# Adds a newline character before each prompt line
SPACESHIP_PROMPT_ADD_NEWLINE=false
# Suffix after prompt character
SPACESHIP_CHAR_SUFFIX=" "
# Prompt character to be shown before any command
SPACESHIP_CHAR_SYMBOL="⇌"

## Vi mode related
SPACESHIP_VI_MODE_SUFFIX=" "
# Text to be shown when in insert mode
SPACESHIP_VI_MODE_INSERT=""
# Text to be shown when in normal mode
SPACESHIP_VI_MODE_NORMAL=""
# Section's color
SPACESHIP_VI_MODE_COLOR="green"

# Jobs related
# Number of jobs after which job count will be shown
SPACESHIP_JOBS_AMOUNT_THRESHOLD="0"
# Symbol displayed when jobs are hiding
SPACESHIP_JOBS_SYMBOL=""
# Prefix before the number of jobs (between jobs indicator and jobs amount)
SPACESHIP_JOBS_AMOUNT_PREFIX=" "

## Git
# Order of git subsection rendering
SPACESHIP_GIT_ORDER=(git_branch git_commit git_status)
# Show section
SPACESHIP_GIT_COMMIT_SHOW=true
# Render section asynchronously
SPACESHIP_GIT_COMMIT_ASYNC=true
# Color of Git status subsection
SPACESHIP_GIT_STATUS_COLOR="white"
# Section's color
SPACESHIP_GIT_BRANCH_COLOR="green"

## Git status
# Prefix before Git status subsection
SPACESHIP_GIT_STATUS_PREFIX=" "
# Suffix after Git status subsection
SPACESHIP_GIT_STATUS_SUFFIX=""
# Indicator for stashed changes
SPACESHIP_GIT_STATUS_STASHED=" "
# Indicator for unstaged files
SPACESHIP_GIT_STATUS_MODIFIED=""
# Indicator for untracked changes
SPACESHIP_GIT_STATUS_UNTRACKED=""
# Indicator for added changes
SPACESHIP_GIT_STATUS_ADDED=" "
# Indicator for renamed files
SPACESHIP_GIT_STATUS_RENAMED="󰑕 "
# Indicator for deleted files
SPACESHIP_GIT_STATUS_DELETED="󱂥 "
# Indicator for unmerged changes
SPACESHIP_GIT_STATUS_UNMERGED="󰱶"
# Indicator for unpushed changes (ahead of remote branch)
SPACESHIP_GIT_STATUS_AHEAD="󱞿 "
# Indicator for unpulled changes (behind of remote branch)
SPACESHIP_GIT_STATUS_BEHIND="󱞡 "
# Indicator for diverged changes (diverged with remote branch)
SPACESHIP_GIT_STATUS_DIVERGED=" "
# Symbol displayed before the section
SPACESHIP_GIT_SYMBOL=""

SPACESHIP_PROMPT_ORDER=(
  time           # Time stamps section
  vi_mode        # Vi mode indicator
  user           # Username section
  dir            # Current directory section
  # host           # Hostname section
  git            # Git section (git_branch + git_status)
  # hg             # Mercurial section (hg_branch  + hg_status)
  # package        # Package version
  # node           # Node.js section
  # bun            # Bun section
  # deno           # Deno section
  # ruby           # Ruby section
  python         # Python section
  # elm            # Elm section
  # elixir         # Elixir section
  # xcode          # Xcode section
  # xcenv          # xcenv section
  # swift          # Swift section
  # swiftenv       # swiftenv section
  # golang         # Go section
  # perl           # Perl section
  # php            # PHP section
  # rust           # Rust section
  # haskell        # Haskell Stack section
  # scala          # Scala section
  # kotlin         # Kotlin section
  # java           # Java section
  # lua            # Lua section
  # dart           # Dart section
  # julia          # Julia section
  # crystal        # Crystal section
  # docker         # Docker section
  # docker_compose # Docker section
  # aws            # Amazon Web Services section
  # gcloud         # Google Cloud Platform section
  # azure          # Azure section
  venv           # virtualenv section
  # conda          # conda virtualenv section
  # uv             # uv section
  # dotnet         # .NET section
  # ocaml          # OCaml section
  # vlang          # V section
  # zig            # Zig section
  # purescript     # PureScript section
  # erlang         # Erlang section
  # gleam          # Gleam section
  # kubectl        # Kubectl context section
  # ansible        # Ansible section
  # terraform      # Terraform workspace section
  # pulumi         # Pulumi stack section
  # ibmcloud       # IBM Cloud section
  # nix_shell      # Nix shell
  # gnu_screen     # GNU Screen section
  exec_time      # Execution time
  async          # Async jobs indicator
  line_sep       # Line break
  # battery        # Battery level and status
  jobs           # Background jobs indicator
  exit_code      # Exit code section
  sudo           # Sudo indicator
  char           # Prompt character
)
