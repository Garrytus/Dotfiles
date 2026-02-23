# ssh hosts completion
function _gather_ssh_hosts() {
  local config_file="${HOME}/.ssh/config"
  local seen=() all_files=()

  # recursively read config files and follows include directives
  function _read_config() {
    local path=${1}
    [[ -f ${path} ]] || return
    for line in ${(f)"$(< $path)"}; do
      # strip carriage return if present
      line="${line%%$'\r'}"
      [[ "$line" =~ '^Include[[:space:]]+' ]] || continue

      # split on spaces, supports globs
      local inc_paths=(${(z)line})
      # drop 'Include'
      inc_paths=("${(@)inc_paths[2,-1]}")

      for inc in "${inc_paths[@]}"; do
        for real in ${~inc}; do
          [[ -f ${real} && ! ${seen[(r)$real]} ]] && {
            seen+=("${real}")
            _read_config "${real}"
          }
        done
      done
    done
    all_files+=("${path}")
  }

  _read_config "${config_file}"

  # extract hostnames
  awk '
  tolower($1) == "host" {
      for (i = 2; i <= NF; i++) {
      gsub(/\r$/, "", $i)         # strip \r
      gsub(/\*$/, "", $i)         # remove trailing *
      print $i
      }
  }
  ' ${(q)all_files} | sort -u
}

# enable dynamic ssh host completion
zstyle ':completion:*:*:ssh:*' hosts $(_gather_ssh_hosts)
